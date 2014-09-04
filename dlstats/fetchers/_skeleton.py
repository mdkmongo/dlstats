#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import pymongo
from dlstats import configuration

class Skeleton(object):
    """Basic structure for statistical providers implementations."""
    def __init__(self):
        self.configuration = configuration
        self.client = pymongo.MongoClient(**self.configuration['MongoDB'])
    def upsert_categories(self,id):
        """Upsert the categories in MongoDB
        """
        raise NotImplementedError("This method from the Skeleton class must"
                                  "be implemented.")
    def upsert_a_series(self,id):
        """Upsert the series in MongoDB
        """
        raise NotImplementedError("This method from the Skeleton class must"
                                  "be implemented.")
    def upsert_dataset(self,id):
        """Upsert a dataset in MongoDB
        """
        raise NotImplementedError("This method from the Skeleton class must"
                                  "be implemented.")
    def _bson_update(self,coll,bson,key):
        old_bson = coll.find_one({key: bson[key]})
        if old_bson == None:
            _id = coll.insert(bson)
            return _id
        else:
            identical = True
            for k in bson.keys():
                if not (k == 'versionDate'):
                    if (old_bson[k] != bson[k]):
                        self.log_warning(coll.database.name+'.'+coll.name+': '+k+" has changed value. Old value: {}, new value: {}".format(old_bson[k],bson[k]))
                        identical = False
            if not identical:
                coll.update({'_id': old_bson['_id']},bson)
            return old_bson['_id']

    def _series_update(self,coll,bson,key):
        old_bson = coll.find_one({key: bson[key]})
        if old_bson == None:
            _id = coll.insert(bson)
            return _id
        else:
            identical = True
            for k in bson.keys():
                if (k != 'versionDate'):
                    if (old_bson[k] != bson[k]):
                        self.log_warning(coll.database.name+'.'+coll.name+': '+k+" has changed value. Old value: {}, new value: {}".format(old_bson[k],bson[k]))
                        identical = False
            if not identical:
                values = bson['values']
                old_values = old_bson['values']
                releaseDates = bson['releaseDates']
                old_releaseDates = old_bson['releaseDates']
                old_revisions = old_bson['revisions']
                for i in range(len(old_values)):
                    if old_values[i] == values[i]:
                        releaseDates[i] = old_releaseDates[i]
                    else:
                        revisions[i] = old_revisions[i]
                        revisions[i][releaseDates[i]] = old_values[i]
                bson['releaseDates'] = releaseDates
                bson['revisions'] = revisions
                coll.update({'_id': old_bson['_id']},bson,upsert=True)
            return old_bson['_id']

    class _Series(self):
        
        def __init__(self):
            self = {'name': None,
                    'key': None,
                    'datasetCode': None,
                    'startDate': None, 
                    'endDate': None, 
                    'values': None,
                    'attributes', None,
                    'releaseDates': None,
                    'revisions': None,
                    'frequency': None,
                    'dimensions': None}
                    # Do we need it?
                    'categoryCode': None,

    class _Dataset():
        def __init__(self):
            self = {'datasetCode': None,
                    'dimensionList': None,
                    'docHref': None,
                    'attributeList': None,
                    'lastUdpate': None,
                    'versionDate': None}

    class _Category():
        def __init__(self):
            self = {'name': None,
                    'children': None,
                    'categoryCode': None,
                    # we need to keep track of wich categories we mirror on Widukind
                    'present': False}