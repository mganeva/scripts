import numpy as np
import lxml.etree as ET

idfpath = '/home/mary/.mantid/instrument/TOFTOF_Definition.xml'

root = ET.parse(idfpath)

for component in root.iter('{http://www.mantidproject.org/IDF/1.0}type'):
    name = component.get('name')
    if ('rack') in name:
        phi = 0.0
        if 'bank_2' in name:
            phi = np.radians(-7.8)
        elif 'bank_3' in name:
            phi = np.radians(7.8)
        elif 'bank_4' in name:
            phi = np.radians(15.6)
        for node in component:
            for subnode in node.iter('{http://www.mantidproject.org/IDF/1.0}location'):
                theta = np.radians(float(subnode.get('t')))
                # phi = np.radians(float(subnode.get('p')))
                
                u0 = np.cos(0.5*theta)*np.sin(0.5*phi)
                u1 = np.cos(0.5*theta)*np.cos(0.5*phi)
                u2 = np.sin(0.5*theta)*np.sin(0.5*phi)
                u3 = -1.0*np.sin(0.5*theta)*np.cos(0.5*phi)
            
                angle = 2.0*np.arccos(u0)
                x = u1/np.sin(0.5*angle)
                y = u2/np.sin(0.5*angle)
                z = u3/np.sin(0.5*angle)
                attrib = {'axis-x': '{0:.3f}'.format(x), 
                          'axis-y': '{0:.3f}'.format(y), 
                          'axis-z': '{0:.3f}'.format(z), 
                          'val': '{0:.3f}'.format(np.degrees(angle))}
                ET.SubElement(subnode, 'rot', attrib)


with open('/home/mary/.mantid/instrument/TOFTOF_Definition_New.xml', 'wb') as outf:
    outf.write(ET.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True, method='xml'))
