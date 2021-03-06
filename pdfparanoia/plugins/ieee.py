# -*- coding: utf-8 -*-

from copy import copy

from ..parser import parse_content
from ..eraser import remove_object_by_id
from ..plugin import Plugin

class IEEEXplore(Plugin):
    """
    IEEE Xplore
    ~~~~~~~~~~~~~~~

    """

    @staticmethod
    def scrub(content):
        evil_ids = []

        # parse the pdf into a pdfminer document
        pdf = parse_content(content)

        # get a list of all object ids
        xrefs = pdf._parser.read_xref()
        xref = xrefs[0]
        objids = xref.get_objids()

        # check each object in the pdf
        for objid in objids:
            # get an object by id
            obj = pdf.getobj(objid)

            if hasattr(obj, "attrs"):
                # watermarks tend to be in FlateDecode elements
                if obj.attrs.has_key("Filter") and str(obj.attrs["Filter"]) == "/FlateDecode":
                    #length = obj.attrs["Length"]
                    #rawdata = copy(obj.rawdata)
                    data = copy(obj.get_data())

                    if "Authorized licensed use limited to: " in data:
                        evil_ids.append(objid)

        for objid in evil_ids:
            print "evil id: " + str(objid)
            content = remove_object_by_id(content, objid)

        return content

