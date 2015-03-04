#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Entitlements(object):
    '''
    Apple's app entitlements.
    '''
    def __init__(self, application_identifier, get_task_allow, keychain_access_groups):
        '''
        :param application_identifier: application identifier
        :type application_identifier: str
        :param get_task_allow: get-task-allow
        :type get_task_allow: bool
        :param keychain_access_groups: keychain access groups
        :type keychain_access_groups: list of str
        :returns: instance
        :rtype: provisioning.entitlements.Entitlements
        '''
        self._application_identifier = application_identifier
        self._get_task_allow = get_task_allow
        self._keychain_access_groups = keychain_access_groups

    @classmethod
    def from_dict(cls, d):
        '''
        :param d: dictionary
        :type d: dict
        :returns: instance
        :rtype: provisioning.entitlements.Entitlements
        '''
        return cls(d['application-identifier'], d['get-task-allow'], d['keychain-access-groups'])

    @property
    def application_identifier(self):
        '''
        :returns: application identifier
        :rtype: str
        '''
        return self._application_identifier

    @property
    def get_task_allow(self):
        '''
        :returns: get-task-allow
        :rtype: bool
        '''
        return self._get_task_allow

    @property
    def keychain_access_groups(self):
        '''
        :returns: keychain access groups
        :rtype: list of str
        '''
        return self._keychain_access_groups

