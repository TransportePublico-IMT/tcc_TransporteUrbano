import xmltodict
import json
import re
from dotenv import load_dotenv
import os
from os.path import join, dirname
import requests, zipfile, io

# Create .env file path.
dotenv_path = join(dirname(__file__), '../.ENV')
# Load file from the path.
load_dotenv(dotenv_path)

def remove_html_from_string(string):
    ret = re.sub('<[^<]+?>', ' ', string)
    ret = re.sub(' +', ' ', ret).strip()
    return ret

def kml_to_dict(kml):
    kml_json = json.loads(json.dumps(xmltodict.parse(kml)))
    return kml_json

def get_infos_from_description(description):
    try:
        vel_trecho = re.search('média do trecho(.*)km/h Tempo', description).group(1).strip()
    except AttributeError:
        vel_trecho = None
    try:
        vel_via = re.search('média da via:(.*)km/h', description).group(1).strip()
    except AttributeError:
        try:
            vel_via = re.search('média do corredor:(.*)km/h', description).group(1).strip()
        except AttributeError:
            vel_via = None
    try:
        trecho = re.search('Trecho:(.*)Referência', description).group(1).strip()
    except AttributeError:
        trecho = None
    try:
        extensao = re.search('\(metros\):(.*)Velocidade média do trecho', description).group(1).replace(',', '').replace('.', '').strip()
    except AttributeError:
        extensao = None
    try:
        tempo = re.search('percurso(.*)Velocidade', description).group(1).replace('h', ':').strip()
        if tempo == '--':
            tempo = None
    except AttributeError:
        tempo = None

    ret = {'vel_trecho': vel_trecho,
            'vel_via': vel_via,
            'trecho': trecho,
            'extensao': extensao,
            'tempo': tempo}
    
    return ret

def clear_coordinates_info(coordinates):
    coordinates = coordinates.replace(',0', '').replace('\t', '').replace(' ', '').split('\n')
    list_lat_lon = []
    for i in coordinates:
        lat_lon = i.split(',')
        if lat_lon[0] == '' or lat_lon[1] == '':
            dict_lat_lon = {'lat': None, 'lon': None}
            list_lat_lon.append(dict_lat_lon)
        else:
            dict_lat_lon = {'lat': lat_lon[1], 'lon': lat_lon[0]}
            list_lat_lon.append(dict_lat_lon)
    return list_lat_lon

def get_kml_dict_info(kml_dict):
    #Estrutura --> ['kml']['Document']['Folder'][0]['Placemark'][0]['name']
    list_infos = []
    folder = kml_dict['kml']['Document']['Folder']
    for i in folder:
        if type(i['Placemark']) == list:
            for j in i['Placemark']:
                name = j['name']

                description = remove_html_from_string(j['description'])
                infos_description = get_infos_from_description(description)

                if 'MultiGeometry' in j:
                    coordinates = ''
                    len_elements = len(j['MultiGeometry']['LineString'])
                    count = 1
                    for k in j['MultiGeometry']['LineString']:
                        coordinates += k['coordinates']
                        if count < len_elements:
                            #salva uma coordenada como nulo para separar elementos do multigeometry
                            coordinates += '\n\n'
                        count += 1
                    coordinates_list = clear_coordinates_info(coordinates)           
                else:
                    coordinates = j['LineString']['coordinates']
                    coordinates_list = clear_coordinates_info(coordinates)

                info = {'name': name,
                        'description': infos_description,
                        'coordinates': coordinates_list}
                list_infos.append(info)
        else:
            name = i['Placemark']['name']

            description = remove_html_from_string(i['Placemark']['description'])
            infos_description = get_infos_from_description(description)
            
            if 'MultiGeometry' in i['Placemark']:
                coordinates = ''
                len_elements = len(i['Placemark']['MultiGeometry']['LineString'])
                count = 1
                for k in i['Placemark']['MultiGeometry']['LineString']:
                    coordinates += k['coordinates']
                    if count < len_elements:
                        #salva uma coordenada como nulo para separar elementos do multigeometry
                        coordinates += '\n\n'
                    count += 1
                coordinates_list = clear_coordinates_info(coordinates)          
            else:
                coordinates = i['Placemark']['LineString']['coordinates']
                coordinates_list = clear_coordinates_info(coordinates)

            info = {'name': name,
                    'description': infos_description,
                    'coordinates': coordinates_list}
            list_infos.append(info)

    return list_infos

def get_kml():
    pre_response = requests.post('http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token='+os.getenv('OLHOVIVO'))
    response = requests.get('http://api.olhovivo.sptrans.com.br/v2.1/KMZ', cookies=pre_response.cookies)
    zipDocument = zipfile.ZipFile(io.BytesIO(response.content))
    for name in zipDocument.namelist():
        if name == 'TA.kml':
            uncompressed = zipDocument.read(name)
            return uncompressed

def get_kml_json():
    kml = get_kml()
    kml_dict = kml_to_dict(kml)
    infos = get_kml_dict_info(kml_dict)
    return json.dumps({'o': infos})

def popular_onibus_velocidade():
    data = get_kml_json()
    url = "http://localhost/api/onibus-velocidade/"
    headers = {
        'Content-Type': 'application/json',
        'Connection' : 'keep-alive',
        'Accept': "*/*"
    }
    r = requests.post(url, data=data, headers=headers)
    return r.json()