#!/usr/bin/env python
# -*- coding:utf-8 -*-

import plistlib
import uuid
import getpass
import platform
import os
from datetime import datetime
from OpenSSL.crypto import FILETYPE_ASN1, load_certificate
from entitlements import Entitlements


class ProvisioningProfile(object):
    '''
    Apple's provisioning profile.
    '''
    def __init__(self, data):
        self._data = data
        self._plist = self._extract_plist(data)
        self._developer_certificates = None
        self._entitlements = None
        self._uuid = None

    def is_expired(self, date=datetime.now()):
        '''
        :param date: date to compare
        :type date: datetime.datetime
        :returns: True if expired
        :rtype: bool
        '''
        return self.expiration_date < date

    def _extract_plist(self, data):
        '''
        Simplified-PKCS7 DEFINITIONS EXPLICIT TAGS ::= BEGIN
        SignedXML ::= SEQUENCE {
            contentType OBJECT IDENTIFIER, -- { 1 2 840 113549 1 7 2 }
            content [0] SEQUENCE {
                version INTEGER,
                digestAlgorithms ANY,
                contentInfo SEQUENCE {
                    contentType OBJECT IDENTIFIER, -- { 1 2 840 113549 1 7 1 }
                    contentXML [0] OCTET STRING
                },
                ...
            }
        }
        END
        '''
        try:
            from pyasn1.codec.der import decoder
        except ImportError:
            plist = data[62, data.rfind('</plist>')]
        else:
            plist = str(decoder.decode(data)[0][1][2][1])
        return plistlib.readPlistFromString(plist)

    @property
    def data(self):
        '''
        :returns: encrypted binary
        :rtype: str
        '''
        return self._data

    @property
    def application_identifier_prefix(self):
        '''
        :returns: ApplicationIdentifierPrefix
        :rtype: str
        '''
        return self._plist['ApplicationIdentifierPrefix']

    @property
    def creation_date(self):
        '''
        :returns: CreationDate
        :rtype: datetime.datetime
        '''
        return self._plist['CreationDate']

    @property
    def developer_certificates(self):
        '''
        :returns: DeveloperCertificates
        :rtype: list of OpenSSL.crypto.X509 instance
        '''
        if self._developer_certificates is None:
            self._developer_certificates = []
            for item in self._plist['DeveloperCertificates']:
                certificate = load_certificate(FILETYPE_ASN1, item.data)
                self._developer_certificates.append(certificate)
        return self._developer_certificates

    @property
    def entitlements(self):
        '''
        :returns: Entitlements
        :rtype: provisioning.entitlements.Entitlements
        '''
        if self._entitlements is None:
            self._entitlements = Entitlements.from_dict(self._plist['Entitlements'])
        return self._entitlements

    @property
    def expiration_date(self):
        '''
        :returns: ExpirationDate
        :rtype: datetime.datetime
        '''
        return self._plist['ExpirationDate']

    @property
    def name(self):
        '''
        :returns: Name
        :rtype: str
        '''
        return self._plist['Name']

    @property
    def provisioned_devices(self):
        '''
        :returns: UDIDs of ProvisionedDevices
        :rtype: list of str
        '''
        return self._plist['ProvisionedDevices']

    @property
    def time_to_live(self):
        '''
        :returns: TimeToLive
        :rtype: int
        '''
        return self._plist['TimeToLive']

    @property
    def uuid(self):
        '''
        :returns: UUID
        :rtype: uuid.UUID
        '''
        if self._uuid is None:
            self._uuid = uuid.UUID(self._plist['UUID'])
        return self._uuid

    @property
    def version(self):
        '''
        :returns: Version
        :rtype: str
        '''
        return str(self._plist['Version'])


PROVISIONING_PROFILES_DIR = '/Users/{user}/Library/MobileDevice/Provisioning Profiles'


def stored_provisioning_profiles(user=getpass.getuser()):
    '''
    :param user: user
    :type user: str
    :returns: ProvisioningProfiles stored in user directory
    :rtype: list of provisioning.profile.ProvisioningProfile
    '''
    if platform.system() != 'Darwin':
        raise OSError('only permitted on OSX.')
    base_path = PROVISIONING_PROFILES_DIR.format(user=user)
    provisioning_profiles = []
    for item in os.listdir(base_path):
        path = os.path.join(base_path, item)
        if path.endswith('.provisioningprofile') or path.endswith('.mobileprovision'):
            with open(path) as f:
                data = f.read()
            provisioning_profiles.append(ProvisioningProfile(data))
    return provisioning_profiles

