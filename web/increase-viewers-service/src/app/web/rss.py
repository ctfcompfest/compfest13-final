import pycurl
from io import BytesIO
from lxml import etree
from urllib.parse import urlparse

class PycurlResolver(etree.Resolver):
    def resolve(self, url, id, context):
        if urlparse(url).scheme == "":
            return None
        buffer = BytesIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        curl.setopt(pycurl.TIMEOUT, 1)
        try:
            curl.perform()
            curl.close()
        except pycurl.error:
            pass
        return self.resolve_string(buffer.getvalue().decode(), context)

def parse_rss(rss):
    parser = etree.XMLParser(load_dtd=True, no_network=False)
    parser.resolvers.add(PycurlResolver())
    
    rss_doc = etree.parse(BytesIO(rss.encode()), parser=parser)
    root = rss_doc.getroot()

    ret = []
    for channel in root.getchildren():
        channelJson = {"items": []}
        for elm in channel.getchildren():
            if elm.tag == "item":
                itemJson = {}
                for subelm in elm.getchildren():
                    itemJson[subelm.tag] = subelm.text
                channelJson['items'].append(itemJson)
            else: channelJson[elm.tag] = elm.text            
        ret.append(channelJson)
    return ret