#!/usr/bin/env python3
# Generator of content/26.1.3/{en,es,pt-BR}.json: the 26.1.2 notes plus what 26.1.3 changes, and of the issues fixed in 26.1.3.
# Reads the facts of the build from tools_2613_data.json. Does NOT touch content/releases.json unless called with --publish.
import json, copy, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = ('en', 'es', 'pt-BR')
DATA = json.load(open('tools_2613_data.json')) if os.path.exists('tools_2613_data.json') else {}


def t(en, es, pt):
    return {'en': en, 'es': es, 'pt-BR': pt}


IMPROVED = [
 t(('System > Update installs the fixes of the firewall', 'Check for updates now finds the packages of the firewall, shows no error the first time, and installs them. The package index of the update server was incomplete and the image trusted a different key from the one that signs the updates; both are fixed, so any later fix can reach the firewalls from this page.'),
   ('Sistema > Actualización instala las correcciones del firewall', 'Buscar actualizaciones ahora encuentra los paquetes del firewall, no muestra error la primera vez y los instala. El índice de paquetes del servidor de actualizaciones estaba incompleto y la imagen confiaba en una clave distinta de la que firma las actualizaciones; las dos cosas están corregidas, así que cualquier corrección posterior puede llegar a los firewalls desde esta página.'),
   ('Sistema > Atualização instala as correções do firewall', 'Verificar atualizações agora encontra os pacotes do firewall, não mostra erro na primeira vez e os instala. O índice de pacotes do servidor de atualizações estava incompleto e a imagem confiava em uma chave diferente da que assina as atualizações; as duas coisas estão corrigidas, então qualquer correção posterior pode chegar aos firewalls por esta página.')),
 t(('The IPS shows the rules it really loads', 'The number of rules on the Dashboard is now the number of rules loaded for the chosen policy, the same as on the IPS Settings tab (before it counted the rules of the catalog that only raise an alert).'),
   ('El IPS muestra las reglas que realmente carga', 'El número de reglas del Panel es ahora el número de reglas cargadas para la política elegida, el mismo que en la pestaña Ajustes del IPS (antes contaba las reglas del catálogo que solo generan una alerta).'),
   ('O IPS mostra as regras que realmente carrega', 'O número de regras do Painel agora é o número de regras carregadas para a política escolhida, o mesmo da aba Ajustes do IPS (antes contava as regras do catálogo que só geram um alerta).')),
 t(('Top talkers stay correct on a busy network', 'With many connections the statistics window of the traffic engine could be read as one second or less, which showed a rate several times too high, or an empty list. The window is now at least ten seconds and measured to the millisecond.'),
   ('Los principales consumidores se mantienen correctos en una red con mucho tráfico', 'Con muchas conexiones la ventana de estadísticas del motor de tráfico podía leerse como un segundo o menos, lo que mostraba una tasa varias veces mayor, o una lista vacía. La ventana ahora es de al menos diez segundos y se mide al milisegundo.'),
   ('Os maiores consumidores permanecem corretos em uma rede com muito tráfego', 'Com muitas conexões a janela de estatísticas do motor de tráfego podia ser lida como um segundo ou menos, o que mostrava uma taxa várias vezes maior, ou uma lista vazia. A janela agora tem pelo menos dez segundos e é medida ao milissegundo.')),
 t(('Fewer \"Unknown\" in the reports', 'Traffic to a site the application catalog does not know is listed under the domain of the site (for example example.com) instead of \"Unknown\". The catalog also has a Nexwall application, so the traffic of the firewall to its own services is classified.'),
   ('Menos \"Desconocido\" en los informes', 'El tráfico hacia un sitio que el catálogo de aplicaciones no conoce se muestra bajo el dominio del sitio (por ejemplo ejemplo.com) en lugar de \"Desconocido\". El catálogo también tiene una aplicación Nexwall, así que se clasifica el tráfico del firewall hacia sus propios servicios.'),
   ('Menos \"Desconhecido\" nos relatórios', 'O tráfego para um site que o catálogo de aplicações não conhece aparece sob o domínio do site (por exemplo exemplo.com) em vez de \"Desconhecido\". O catálogo também tem uma aplicação Nexwall, então o tráfego do firewall para os próprios serviços é classificado.')),
 t(('Threat Analytics shows the real state of the sandbox', 'The Sandbox stage says whether the sandbox is working, not enabled on this firewall, or not in the plan. Only Advanced Threat Protection and Collective Defense are marked as coming.'),
   ('Threat Analytics muestra el estado real del sandbox', 'La etapa Sandbox dice si el sandbox funciona, si no está activado en este firewall o si no está en el plan. Solo Advanced Threat Protection y Collective Defense aparecen como próximamente.'),
   ('O Threat Analytics mostra o estado real do sandbox', 'A etapa Sandbox diz se o sandbox está funcionando, se não está ativado neste firewall ou se não está no plano. Apenas o Advanced Threat Protection e o Collective Defense aparecem como em breve.')),
]
# t(...) above was given tuples per language: normalise to {'en': (title, body)}
IMPROVED = [{k: v for k, v in zip(L, item)} if not isinstance(item, dict) else item for item in IMPROVED]

OVERVIEW_PREFIX = t(
 'Nexwall Firewall 26.1.3 completes version 26 of the firewall. It is 26.1.2 with the updates working: the update server is complete, the image trusts the Nexwall package key, and the firewall can be fixed from System > Update. It also corrects the rule count of the IPS on the Dashboard, the Top talkers readings on a busy network and the Sandbox stage of Threat Analytics, and names unknown traffic by its domain. ',
 'Nexwall Firewall 26.1.3 completa la versión 26 del firewall. Es la 26.1.2 con las actualizaciones funcionando: el servidor de actualizaciones está completo, la imagen confía en la clave de paquetes de Nexwall y el firewall puede corregirse desde Sistema > Actualización. También corrige el número de reglas del IPS en el Panel, las lecturas de los principales consumidores en una red con mucho tráfico y la etapa Sandbox de Threat Analytics, y nombra el tráfico desconocido por su dominio. ',
 'O Nexwall Firewall 26.1.3 completa a versão 26 do firewall. É a 26.1.2 com as atualizações funcionando: o servidor de atualizações está completo, a imagem confia na chave de pacotes da Nexwall e o firewall pode ser corrigido por Sistema > Atualização. Também corrige o número de regras do IPS no Painel, as leituras dos maiores consumidores em uma rede com muito tráfego e a etapa Sandbox do Threat Analytics, e nomeia o tráfego desconhecido pelo domínio. ')
SUMMARY = t(
 'The final release of version 26: the 26.1.2 features with working package updates, a complete update server, and corrections to the IPS rule count, Top talkers and Threat Analytics.',
 'La versión final de la 26: las funciones de la 26.1.2 con actualizaciones de paquetes que funcionan, un servidor de actualizaciones completo y correcciones del número de reglas del IPS, los principales consumidores y Threat Analytics.',
 'A versão final da 26: os recursos da 26.1.2 com atualizações de pacotes funcionando, um servidor de atualizações completo e correções do número de regras do IPS, dos maiores consumidores e do Threat Analytics.')
STATUS = t('Stable: image and installer ISO built and tested', 'Estable: imagen e ISO de instalación construidas y probadas', 'Estável: imagem e ISO de instalação construídas e testadas')
TIMELINE = t(('2026-10-13', 'From 26.1.2 to 26.1.3', 'The package update path (complete index, Nexwall key in the image), the corrections found after 26.1.2 was published (IPS rule count, Top talkers window, Threat Analytics stages, unknown applications) and the Nexwall application in the catalog.'),
             ('2026-10-13', 'De 26.1.2 a 26.1.3', 'La vía de actualización de paquetes (índice completo, clave de Nexwall en la imagen), las correcciones encontradas tras publicar la 26.1.2 (número de reglas del IPS, ventana de los principales consumidores, etapas de Threat Analytics, aplicaciones desconocidas) y la aplicación Nexwall en el catálogo.'),
             ('2026-10-13', 'De 26.1.2 a 26.1.3', 'O caminho de atualização de pacotes (índice completo, chave da Nexwall na imagem), as correções encontradas após a 26.1.2 ser publicada (número de regras do IPS, janela dos maiores consumidores, etapas do Threat Analytics, aplicações desconhecidas) e a aplicação Nexwall no catálogo.'))
UPGRADE_NOTE = t(
 'A firewall that runs 26.1.2 cannot install package updates (its image trusts another key). Install 26.1.3 from the ISO or the image and restore the configuration from a backup.',
 'Un firewall con la 26.1.2 no puede instalar actualizaciones de paquetes (su imagen confía en otra clave). Instale la 26.1.3 desde la ISO o la imagen y restaure la configuración desde una copia de seguridad.',
 'Um firewall com a 26.1.2 não consegue instalar atualizações de pacotes (sua imagem confia em outra chave). Instale a 26.1.3 pela ISO ou pela imagem e restaure a configuração de um backup.')

for lang in L:
    d = copy.deepcopy(json.load(open('content/26.1.2/%s.json' % lang)))
    d['title'] = 'Nexwall Firewall 26.1.3'
    d['summary'] = SUMMARY[lang]
    first, _, rest = d['overview'].partition('. ')
    d['overview'] = OVERVIEW_PREFIX[lang] + rest
    for row in d['at_a_glance']:
        if row['value'] == '26.1.2':
            row['value'] = '26.1.3'
    d['at_a_glance'][1]['value'] = STATUS[lang]
    imp = [{'tag': 'improved', 'title': it[lang][0], 'body': it[lang][1]} for it in IMPROVED]
    for s in d['sections']:
        if s['id'] == 'improvements':
            s['items'] = imp + s['items']
    for r in d['components']['rows']:
        if r['name'] == 'Image':
            r['version'] = '26.1.3'
        elif r['name'] == 'Firmware sources':
            r['version'] = DATA.get('firmware_commit', r['version'])
        elif r['name'] == 'Web interface':
            r['version'] = DATA.get('ui', '3.0.1')
        elif r['name'] == 'Traffic engine plugins':
            r['version'] = DATA.get('plugins', '1.0.4')
    d['timeline']['entries'] = [{'date': TIMELINE[lang][0], 'title': TIMELINE[lang][1], 'text': TIMELINE[lang][2]}] + d['timeline']['entries']
    d['upgrade'].append(UPGRADE_NOTE[lang])
    os.makedirs('content/26.1.3', exist_ok=True)
    json.dump(d, open('content/26.1.3/%s.json' % lang, 'w'), ensure_ascii=False, indent=2)
    open('content/26.1.3/%s.json' % lang, 'a').write('\n')

reg = json.load(open('content/issues.json'))
have = {x['id'] for x in reg['issues']}
FIXED = [
 ('NXW-1038', 'updates', t('Check for updates failed the first time', 'Buscar actualizaciones fallaba la primera vez', 'Verificar atualizações falhava na primeira vez'),
  t('The update server lacked the package index of the kernel modules, so the check ended with an error until a partial copy was cached. The index is published.', 'Al servidor de actualizaciones le faltaba el índice de paquetes de los módulos del kernel, así que la búsqueda terminaba con error hasta que se guardaba una copia parcial. El índice está publicado.', 'O servidor de atualizações não tinha o índice de pacotes dos módulos do kernel, então a verificação terminava com erro até uma cópia parcial ser guardada. O índice está publicado.')),
 ('NXW-1039', 'updates', t('The image of 26.1.2 trusted a different package key', 'La imagen de la 26.1.2 confiaba en otra clave de paquetes', 'A imagem da 26.1.2 confiava em outra chave de pacotes'),
  t('The image was built with a key generated by the build, not the Nexwall key, so package updates signed by Nexwall would be refused. 26.1.3 is built with the Nexwall key. Firewalls on 26.1.2 must be reinstalled with 26.1.3.', 'La imagen se construyó con una clave generada por la compilación, no la clave de Nexwall, así que las actualizaciones de paquetes firmadas por Nexwall serían rechazadas. La 26.1.3 se construye con la clave de Nexwall. Los firewalls con la 26.1.2 deben reinstalarse con la 26.1.3.', 'A imagem foi construída com uma chave gerada pela compilação, não a chave da Nexwall, então as atualizações de pacotes assinadas pela Nexwall seriam recusadas. A 26.1.3 é construída com a chave da Nexwall. Os firewalls com a 26.1.2 devem ser reinstalados com a 26.1.3.')),
 ('NXW-1040', 'dashboard', t('The IPS showed 7,645 rules on the Dashboard and 35,253 on its Settings', 'El IPS mostraba 7.645 reglas en el Panel y 35.253 en sus Ajustes', 'O IPS mostrava 7.645 regras no Painel e 35.253 nos Ajustes'),
  t('The Dashboard counted the alert-only rules of the catalog. It now shows the rules loaded for the chosen policy.', 'El Panel contaba las reglas del catálogo que solo generan alerta. Ahora muestra las reglas cargadas para la política elegida.', 'O Painel contava as regras do catálogo que só geram alerta. Agora mostra as regras carregadas para a política escolhida.')),
 ('NXW-1041', 'monitoring', t('Top talkers could show a rate several times too high, or nothing, under load', 'Los principales consumidores podían mostrar una tasa varias veces mayor, o nada, con carga', 'Os maiores consumidores podiam mostrar uma taxa várias vezes maior, ou nada, sob carga'),
  t('The statistics window could be read as zero or one second. It is now at least ten seconds and measured to the millisecond.', 'La ventana de estadísticas podía leerse como cero o un segundo. Ahora es de al menos diez segundos y se mide al milisegundo.', 'A janela de estatísticas podia ser lida como zero ou um segundo. Agora tem pelo menos dez segundos e é medida ao milissegundo.')),
 ('NXW-1042', 'threat-analytics', t('Threat Analytics said the sandbox was coming', 'Threat Analytics decía que el sandbox llegaba pronto', 'O Threat Analytics dizia que o sandbox estava chegando'),
  t('The Sandbox stage now shows its real state: working, not enabled or not in the plan.', 'La etapa Sandbox ahora muestra su estado real: funcionando, no activado o fuera del plan.', 'A etapa Sandbox agora mostra seu estado real: funcionando, não ativado ou fora do plano.')),
]
for iid, area, title, body in FIXED:
    if iid not in have:
        reg['issues'].append({'id': iid, 'type': 'fixed', 'version': '26.1.3', 'area': area, 'title': title, 'body': body})
json.dump(reg, open('content/issues.json', 'w'), ensure_ascii=False, indent=1)
open('content/issues.json', 'a').write('\n')

if '--publish' in sys.argv:
    rel = json.load(open('content/releases.json'))
    rel = [r for r in rel if r['version'] != '26.1.3']
    for r in rel:
        if r['version'] == '26.1.2':
            r['status'] = 'superseded'
    rel.insert(0, {'version': '26.1.3', 'date': DATA['date'], 'status': 'stable', 'downloads': DATA['downloads']})
    json.dump(rel, open('content/releases.json', 'w'), ensure_ascii=False, indent=1)
    open('content/releases.json', 'a').write('\n')
print('26.1.3 written; issues:', len(reg['issues']))
