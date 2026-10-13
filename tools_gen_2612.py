#!/usr/bin/env python3
# Generator of content/26.1.2/{en,es,pt-BR}.json (from the 26.1.1 notes, which were never published: 26.1.2 is the first release
# with all of it) and of the issues of 26.1.2. Reads the facts of the build from tools_2612_data.json (written when the image and the
# ISO are built). Does NOT touch content/releases.json unless called with --publish.
import json, copy, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
L = ('en', 'es', 'pt-BR')
DATA = json.load(open('tools_2612_data.json')) if os.path.exists('tools_2612_data.json') else {}


def t(en, es, pt):
    return {'en': en, 'es': es, 'pt-BR': pt}


NEW = {
 'rule_model': t(
  ('Web Protection rules: block and inspect are separate choices',
   'In the rule editor every category can be blocked, allowed or inspected on its own. The blocked column and the allowed column each have an "inspect all" switch and a tick for every category: blocking is decided from the server name without opening the connection, and inspecting is what opens a category in the web proxy, for the antivirus, the content filter and the certificate checks in the allowed column, or for the block page in the blocked column. A category that is blocked and not inspected costs the proxy nothing.'),
  ('Reglas de Web Protection: bloquear e inspeccionar son decisiones separadas',
   'En el editor de reglas cada categoría puede bloquearse, permitirse o inspeccionarse por separado. La columna de bloqueadas y la de permitidas tienen cada una un interruptor "inspeccionar todo" y una casilla por categoría: el bloqueo se decide por el nombre del servidor sin abrir la conexión, e inspeccionar es lo que abre una categoría en el proxy web, para el antivirus, el filtro de contenido y las comprobaciones de certificado en la columna de permitidas, o para la página de bloqueo en la de bloqueadas. Una categoría bloqueada y no inspeccionada no cuesta nada al proxy.'),
  ('Regras do Web Protection: bloquear e inspecionar são escolhas separadas',
   'No editor de regras cada categoria pode ser bloqueada, permitida ou inspecionada por conta própria. A coluna de bloqueadas e a de permitidas têm, cada uma, um interruptor "inspecionar tudo" e uma caixa por categoria: o bloqueio é decidido pelo nome do servidor sem abrir a conexão, e inspecionar é o que abre uma categoria no proxy web, para o antivírus, o filtro de conteúdo e as verificações de certificado na coluna de permitidas, ou para a página de bloqueio na de bloqueadas. Uma categoria bloqueada e não inspecionada não custa nada ao proxy.')),
 'quic': t(
  ('A QUIC switch in Web Protection',
   'QUIC (HTTP/3) carries web traffic over UDP, where no proxy can read it. The new switch "Block QUIC (HTTP/3)" in the Web Protection settings (on by default) refuses UDP port 443 for the clients of the rules that filter the web, so their browsers use HTTPS over TCP at once and the block pages, SafeSearch, the antivirus and the content filter apply to everything. The refusal now reaches the client at once (see the fixes), so there is no wait before the browser falls back.'),
  ('Un interruptor de QUIC en Web Protection',
   'QUIC (HTTP/3) lleva el tráfico web sobre UDP, donde ningún proxy puede leerlo. El nuevo interruptor "Bloquear QUIC (HTTP/3)" de los ajustes de Web Protection (activado por defecto) rechaza el puerto UDP 443 de los clientes de las reglas que filtran la web, de modo que sus navegadores usan HTTPS sobre TCP de inmediato y las páginas de bloqueo, SafeSearch, el antivirus y el filtro de contenido se aplican a todo. El rechazo ahora llega al cliente al instante (vea las correcciones), así que el navegador no espera antes de cambiar.'),
  ('Um interruptor de QUIC no Web Protection',
   'O QUIC (HTTP/3) leva o tráfego web sobre UDP, onde nenhum proxy consegue lê-lo. O novo interruptor "Bloquear QUIC (HTTP/3)" nas configurações do Web Protection (ativado por padrão) recusa a porta UDP 443 dos clientes das regras que filtram a web, de modo que seus navegadores usam HTTPS sobre TCP na hora e as páginas de bloqueio, o SafeSearch, o antivírus e o filtro de conteúdo valem para tudo. A recusa agora chega ao cliente na hora (veja as correções), então o navegador não espera antes de trocar.')),
 'badges': t(
  ('What is really running, not only what is switched on',
   'The pages of Application Control, Network Protection (IPS), Web Protection and the antivirus show a badge that is green only when the service is running (its process is up and bound to what it needs); a service that is switched on but not running turns red. The reading comes from the firewall itself (processes and traffic queues) and is the same one the Dashboard uses.'),
  ('Lo que realmente está en ejecución, no solo lo que está activado',
   'Las páginas de Control de aplicaciones, Protección de red (IPS), Web Protection y el antivirus muestran una insignia que solo es verde cuando el servicio está en ejecución (su proceso está activo y enlazado a lo que necesita); un servicio activado pero que no se ejecuta se pone en rojo. La lectura viene del propio firewall (procesos y colas de tráfico) y es la misma que usa el Panel.'),
  ('O que realmente está em execução, não só o que está ligado',
   'As páginas de Controle de aplicações, Proteção de rede (IPS), Web Protection e do antivírus mostram um selo que só é verde quando o serviço está em execução (o processo está ativo e ligado ao que precisa); um serviço ligado que não está rodando fica vermelho. A leitura vem do próprio firewall (processos e filas de tráfego) e é a mesma que o Painel usa.')),
 'vpn_clients': t(
  ('Nexwall VPN clients on the Remote Access page',
   'The Remote Access (OpenVPN) page lists the latest builds of the Nexwall VPN clients for your users: Windows (64-bit Intel / AMD, ARM64 and 32-bit), Android, and Linux packages for Debian and Ubuntu (64-bit Intel / AMD and ARM64). The macOS client is not published yet. The clients are test builds and are not code-signed.'),
  ('Clientes VPN de Nexwall en la página de Acceso remoto',
   'La página de Acceso remoto (OpenVPN) lista las últimas compilaciones de los clientes VPN de Nexwall para sus usuarios: Windows (Intel / AMD de 64 bits, ARM64 y 32 bits), Android y paquetes de Linux para Debian y Ubuntu (Intel / AMD de 64 bits y ARM64). El cliente de macOS aún no está publicado. Los clientes son compilaciones de prueba y no están firmados.'),
  ('Clientes VPN da Nexwall na página de Acesso remoto',
   'A página de Acesso remoto (OpenVPN) lista as últimas versões dos clientes VPN da Nexwall para seus usuários: Windows (Intel / AMD de 64 bits, ARM64 e 32 bits), Android e pacotes Linux para Debian e Ubuntu (Intel / AMD de 64 bits e ARM64). O cliente para macOS ainda não foi publicado. Os clientes são versões de teste e não são assinados.')),
}

# the interface item of 26.1.1 becomes the 3.0 one
DASHBOARD = t(
 ('A redesigned interface (3.0)',
  'One blue family in light and dark mode: a pale blue menu and top bar in light mode, a navy interface in dark mode, a blue accent, and a page, card and table style that is the same everywhere. The top bar has the page path, a search (Ctrl+K), the language, help, the status center with the alerts of the firewall and the unit chip with the health dot, serial number, version, uptime and license. Every page opens with its tabs, then one paragraph that says what the page is for; the pages of the Policy section have tighter table rows, the side panels follow the density of the menu, and Firewall Rules and Zones & Policies have a column of summary cards on the right (rules by action, busiest zone pairs, tags that filter the list with a click). The Dashboard shows the protection of the firewall in one view and the traffic of today, 7 or 30 days. The Web Protection settings have an engine monitor, rules are deleted from a three-dots menu so that it is harder to do by mistake, and the Monitor tabs follow the same design.'),
 ('Una interfaz rediseñada (3.0)',
  'Una sola familia de azules en modo claro y oscuro: menú y barra superior azul pálido en modo claro, interfaz azul marino en modo oscuro, un acento azul y un estilo de página, tarjetas y tablas igual en todas partes. La barra superior tiene la ruta de la página, una búsqueda (Ctrl+K), el idioma, la ayuda, el centro de estado con las alertas del firewall y el chip de la unidad con el punto de salud, número de serie, versión, tiempo de actividad y licencia. Cada página abre con sus pestañas y luego un párrafo que dice para qué sirve; las páginas de la sección Política tienen filas de tabla más compactas, los paneles laterales siguen la densidad del menú, y Reglas de firewall y Zonas y políticas tienen una columna de tarjetas de resumen a la derecha (reglas por acción, pares de zonas más usados, etiquetas que filtran la lista con un clic). El Panel muestra la protección del firewall en una vista y el tráfico de hoy, 7 o 30 días. Los ajustes de Web Protection tienen un monitor del motor, las reglas se eliminan desde un menú de tres puntos para que sea más difícil hacerlo por error, y las pestañas del Monitor siguen el mismo diseño.'),
 ('Uma interface redesenhada (3.0)',
  'Uma única família de azuis nos modos claro e escuro: menu e barra superior azul pálido no modo claro, interface azul-marinho no modo escuro, um acento azul e um estilo de página, cartões e tabelas igual em todo lugar. A barra superior tem o caminho da página, uma busca (Ctrl+K), o idioma, a ajuda, a central de status com os alertas do firewall e o chip da unidade com o ponto de saúde, número de série, versão, tempo de atividade e licença. Cada página abre com suas abas e depois um parágrafo que diz para que serve; as páginas da seção Política têm linhas de tabela mais compactas, os painéis laterais seguem a densidade do menu, e Regras de firewall e Zonas e políticas têm uma coluna de cartões de resumo à direita (regras por ação, pares de zonas mais usados, tags que filtram a lista com um clique). O Painel mostra a proteção do firewall em uma visão e o tráfego de hoje, 7 ou 30 dias. As configurações do Web Protection têm um monitor do motor, as regras são excluídas por um menu de três pontos para ser mais difícil fazer por engano, e as abas do Monitor seguem o mesmo design.'))

IMPROVED = {
 'stall': t(
  ('The traffic engine no longer stalls under load',
   'Two causes of the engine standing still were found with core dumps from a lab firewall under load and are fixed: two threads waiting for each other inside two of the Nexwall plugins, and the capture thread ending when the kernel dropped a queued packet. A watchdog now checks the engine every minute and, if it stands still, takes the engine out of the path (traffic keeps flowing without analysis) and restarts it, with a cooldown and a limit of restarts per hour. The default when the engine cannot keep up is to let traffic through, not to block it.'),
  ('El motor de tráfico ya no se detiene con carga',
   'Se encontraron y corrigieron, con volcados de memoria de un firewall de laboratorio bajo carga, dos causas de que el motor se quedara parado: dos hilos esperándose entre sí dentro de dos de los plugins de Nexwall, y el hilo de captura que terminaba cuando el kernel descartaba un paquete en cola. Un vigilante ahora revisa el motor cada minuto y, si se detiene, lo saca del camino (el tráfico sigue sin análisis) y lo reinicia, con un tiempo de espera y un límite de reinicios por hora. Por defecto, cuando el motor no da abasto, el tráfico pasa, no se bloquea.'),
  ('O motor de tráfego não trava mais sob carga',
   'Duas causas do motor ficar parado foram encontradas com despejos de memória de um firewall de laboratório sob carga e estão corrigidas: duas threads esperando uma pela outra dentro de dois dos plugins da Nexwall, e a thread de captura terminando quando o kernel descartava um pacote da fila. Um vigia agora verifica o motor a cada minuto e, se ele parar, tira o motor do caminho (o tráfego segue sem análise) e o reinicia, com um tempo de espera e um limite de reinícios por hora. O padrão, quando o motor não dá conta, é deixar o tráfego passar, não bloquear.')),
 'conflict': t(
  ('Sites with changing DNS answers open behind the web proxy',
   'Some sites (streaming services and other CDNs) answer the client and the proxy with different addresses. The proxy used to refuse such an intercepted connection with an error 409, and the site did not load. It now sends the connection to the address the client chose, as it already did for plain HTTP, without caching it.'),
  ('Los sitios con respuestas DNS cambiantes se abren detrás del proxy web',
   'Algunos sitios (servicios de streaming y otras CDN) responden al cliente y al proxy con direcciones distintas. El proxy rechazaba esa conexión interceptada con un error 409 y el sitio no cargaba. Ahora envía la conexión a la dirección que eligió el cliente, como ya hacía con HTTP simple, sin guardarla en la caché.'),
  ('Sites com respostas DNS que mudam abrem atrás do proxy web',
   'Alguns sites (serviços de streaming e outras CDN) respondem ao cliente e ao proxy com endereços diferentes. O proxy recusava essa conexão interceptada com um erro 409 e o site não carregava. Agora ele envia a conexão ao endereço que o cliente escolheu, como já fazia com HTTP simples, sem guardá-la no cache.')),
 'wanlog': t(
  ('Blocked traffic from the internet is in the Log Viewer',
   'The WAN zone now logs what it rejects (at most 10 lines a minute), so the Firewall traffic tab shows blocked traffic and not only the allowed one.'),
  ('El tráfico bloqueado desde internet está en el Visor de registros',
   'La zona WAN ahora registra lo que rechaza (como máximo 10 líneas por minuto), de modo que la pestaña Tráfico del firewall muestra el tráfico bloqueado y no solo el permitido.'),
  ('O tráfego bloqueado vindo da internet está no Visualizador de logs',
   'A zona WAN agora registra o que recusa (no máximo 10 linhas por minuto), de modo que a aba Tráfego do firewall mostra o tráfego bloqueado e não só o permitido.')),
 'icmp': t(
  ('Refusals reach the client at once',
   'The "port unreachable" answer of a rejected connection, and the messages that path MTU discovery needs, were swallowed by the traffic engine queue. They now pass, so a browser whose QUIC is refused changes to HTTPS in a few milliseconds instead of after a timeout.'),
  ('Los rechazos llegan al cliente al instante',
   'La respuesta "puerto inalcanzable" de una conexión rechazada, y los mensajes que necesita el descubrimiento de MTU de la ruta, eran absorbidos por la cola del motor de tráfico. Ahora pasan, de modo que un navegador al que se le rechaza QUIC cambia a HTTPS en unos milisegundos y no después de un tiempo de espera.'),
  ('As recusas chegam ao cliente na hora',
   'A resposta "porta inalcançável" de uma conexão recusada, e as mensagens de que a descoberta de MTU do caminho precisa, eram engolidas pela fila do motor de tráfego. Agora elas passam, de modo que um navegador cujo QUIC é recusado muda para HTTPS em alguns milissegundos e não depois de um tempo limite.')),
 'proxyload': t(
  ('The web proxy keeps working under load',
   'The proxy could run out of open files (a limit of 1,024) and the antivirus connection was switched off for minutes after a burst of failures. The limit is now 16,384, up to 256 files can be scanned at the same time and the scanner connection is retried after 10 seconds.'),
  ('El proxy web sigue funcionando bajo carga',
   'El proxy podía quedarse sin archivos abiertos (un límite de 1.024) y la conexión del antivirus se desactivaba durante minutos tras una ráfaga de fallos. El límite ahora es 16.384, se pueden analizar hasta 256 archivos a la vez y la conexión del analizador se reintenta a los 10 segundos.'),
  ('O proxy web continua funcionando sob carga',
   'O proxy podia ficar sem arquivos abertos (um limite de 1.024) e a conexão do antivírus era desligada por minutos depois de uma rajada de falhas. O limite agora é 16.384, até 256 arquivos podem ser varridos ao mesmo tempo e a conexão do verificador é tentada de novo após 10 segundos.')),
 'wg': t(
  ('WireGuard tunnels keep the internet links apart',
   'A tunnel no longer pins the route to its peer to the internet link that happened to be the default when the tunnel came up. On a firewall with two internet links a stale route of that kind could cut the license, the updates and the threat lists.'),
  ('Los túneles WireGuard no fijan el enlace de internet',
   'Un túnel ya no fija la ruta hacia su par al enlace de internet que era el predeterminado cuando el túnel se levantó. En un firewall con dos enlaces de internet, una ruta obsoleta de ese tipo podía cortar la licencia, las actualizaciones y las listas de amenazas.'),
  ('Os túneis WireGuard não fixam o link de internet',
   'Um túnel não fixa mais a rota para o seu par no link de internet que era o padrão quando o túnel subiu. Em um firewall com dois links de internet, uma rota antiga desse tipo podia cortar a licença, as atualizações e as listas de ameaças.')),
 'dpi': t(
  ('Application Control: an engine switch and a true state',
   'Application Control has an engine switch, Web Protection turns the engine on when it needs it, and the Dashboard and the pages show the real state of Network Protection (IPS) and Application Control. The traffic of the Top talkers card and Traffic Analytics counts the same flows.'),
  ('Control de aplicaciones: un interruptor del motor y el estado real',
   'El Control de aplicaciones tiene un interruptor del motor, Web Protection lo enciende cuando lo necesita, y el Panel y las páginas muestran el estado real de la Protección de red (IPS) y del Control de aplicaciones. El tráfico de la tarjeta Top talkers y de Traffic Analytics cuenta los mismos flujos.'),
  ('Controle de aplicações: um interruptor do motor e o estado real',
   'O Controle de aplicações tem um interruptor do motor, o Web Protection liga o motor quando precisa, e o Painel e as páginas mostram o estado real da Proteção de rede (IPS) e do Controle de aplicações. O tráfego do cartão Top talkers e do Traffic Analytics conta os mesmos fluxos.')),
}
ORDER_NEW = ['block_page', 'content', 'sandbox', 'analytics', 'dashboard', 'rule_model', 'quic', 'badges', 'vpn_clients', 'plots', 'logviewer', 'installer']
ORDER_IMP = ['stall', 'conflict', 'wanlog', 'icmp', 'proxyload', 'wg', 'dpi', 'defaults', 'wan', 'youtube', 'logs']

SUMMARY = t(
 'Web Protection with separate block and inspect choices, block pages, a content filter, files tested in a sandbox, a new interface (3.0) with a blue light and dark theme, a traffic engine that no longer stalls under load, and an installer ISO.',
 'Web Protection con decisiones separadas de bloquear e inspeccionar, páginas de bloqueo, un filtro de contenido, archivos probados en un sandbox, una interfaz nueva (3.0) con tema azul claro y oscuro, un motor de tráfico que ya no se detiene con carga y una ISO de instalación.',
 'Web Protection com escolhas separadas de bloquear e inspecionar, páginas de bloqueio, um filtro de conteúdo, arquivos testados em um sandbox, uma interface nova (3.0) com tema azul claro e escuro, um motor de tráfego que não trava mais sob carga e uma ISO de instalação.')
OVERVIEW = t(
 'Nexwall Firewall 26.1.2 is the first release of the 26.1 series that is published: it carries everything built since 26.1.0. Web Protection decides the block and the inspection of every category separately, a blocked website can show a page that says why, pages can be judged by their content, and files that pass the antivirus can be tested in the Nexwall sandbox. The interface is new (version 3.0, light and dark), Threat Analytics and Traffic Analytics follow the Dashboard, and the Log Viewer lists the web traffic and the traffic the firewall blocks. The traffic engine was hardened against standing still under load, sites with changing DNS answers open behind the web proxy, and the release comes as an installer ISO for virtual machines, USB sticks and appliances.',
 'Nexwall Firewall 26.1.2 es la primera versión de la serie 26.1 que se publica: lleva todo lo construido desde 26.1.0. Web Protection decide por separado el bloqueo y la inspección de cada categoría, un sitio bloqueado puede mostrar una página que dice por qué, las páginas pueden juzgarse por su contenido y los archivos que pasan el antivirus pueden probarse en el sandbox de Nexwall. La interfaz es nueva (versión 3.0, clara y oscura), Threat Analytics y Traffic Analytics siguen al Panel y el Visor de registros lista el tráfico web y el tráfico que bloquea el firewall. El motor de tráfico se reforzó contra detenerse con carga, los sitios con respuestas DNS cambiantes se abren detrás del proxy web y la versión viene como una ISO de instalación para máquinas virtuales, memorias USB y equipos.',
 'O Nexwall Firewall 26.1.2 é a primeira versão da série 26.1 que é publicada: traz tudo o que foi construído desde a 26.1.0. O Web Protection decide separadamente o bloqueio e a inspeção de cada categoria, um site bloqueado pode mostrar uma página que diz por quê, as páginas podem ser julgadas pelo conteúdo e os arquivos que passam pelo antivírus podem ser testados no sandbox da Nexwall. A interface é nova (versão 3.0, clara e escura), o Threat Analytics e o Traffic Analytics seguem o Painel e o Visualizador de logs lista o tráfego web e o tráfego que o firewall bloqueia. O motor de tráfego foi reforçado contra travar sob carga, os sites com respostas DNS que mudam abrem atrás do proxy web e a versão vem como uma ISO de instalação para máquinas virtuais, pendrives e equipamentos.')

STATUS = t('Stable: image and installer ISO built and tested', 'Estável: imagem e ISO de instalação construídas e testadas', 'Estável: imagem e ISO de instalação construídas e testadas')
MEM = t(
 '2 GB of memory without Web Protection; 4 GB or more with the antivirus and the inspection of encrypted traffic, and 8 GB recommended when the antivirus, the inspection, the intrusion prevention and Application Control all run on a busy network (on 4 GB the antivirus engine can be stopped by the system under heavy load).',
 '2 GB de memoria sin Web Protection; 4 GB o más con el antivirus y la inspección del tráfico cifrado, y 8 GB recomendados cuando el antivirus, la inspección, la prevención de intrusiones y el Control de aplicaciones funcionan juntos en una red con mucho tráfico (con 4 GB el sistema puede detener el motor del antivirus bajo carga fuerte).',
 '2 GB de memória sem o Web Protection; 4 GB ou mais com o antivírus e a inspeção do tráfego criptografado, e 8 GB recomendados quando o antivírus, a inspeção, a prevenção de intrusões e o Controle de aplicações funcionam juntos em uma rede com muito tráfego (com 4 GB o sistema pode parar o motor do antivírus sob carga pesada).')

COMPONENTS = {   # name -> (version, note per language or None)
 'Web interface': ('3.0.0', None),
 'Web Protection': ('0.10.0', t('Categories, profiles, block and inspect per category, block page, content filter, sandbox client, inspection, antivirus control, SafeSearch, YouTube and QUIC options',
                               'Categorías, perfiles, bloquear e inspeccionar por categoría, página de bloqueo, filtro de contenido, cliente del sandbox, inspección, control del antivirus, opciones de SafeSearch, YouTube y QUIC',
                               'Categorias, perfis, bloquear e inspecionar por categoria, página de bloqueio, filtro de conteúdo, cliente do sandbox, inspeção, controle do antivírus, opções de SafeSearch, YouTube e QUIC')),
 'Web proxy': ('Squid 7.1', t('Inspection of encrypted traffic, one certificate authority per firewall; intercepted tunnels follow the client\'s destination',
                              'Inspección del tráfico cifrado, una autoridad certificadora por firewall; los túneles interceptados siguen el destino del cliente',
                              'Inspeção do tráfego criptografado, uma autoridade certificadora por firewall; os túneis interceptados seguem o destino do cliente')),
 'Traffic classification engine': ('5.2.8 (release 8)', None),
 'Traffic engine plugins': (DATA.get('plugins', '1.0.3'), None),
}
if DATA.get('plugins'):
    pass

TIMELINE = t(
 ('2026-10-07 to 13', 'From 26.1.0 to 26.1.2', 'Everything of 26.1.1 (block page, content filter, sandbox client, Threat Analytics and Traffic Analytics, new dashboard and plots, Log Viewer tabs, default WAN) and the work of the week after the lab tests: the engine stalls found and fixed, the interface 3.0, the new rule model, the proxy fixes under load and for changing DNS answers, the VPN client downloads and the installer ISO.'),
 ('2026-10-07 a 13', 'De 26.1.0 a 26.1.2', 'Todo lo de 26.1.1 (página de bloqueo, filtro de contenido, cliente del sandbox, Threat Analytics y Traffic Analytics, panel y gráficos nuevos, pestañas del Visor de registros, WAN por defecto) y el trabajo de la semana tras las pruebas de laboratorio: las detenciones del motor encontradas y corregidas, la interfaz 3.0, el nuevo modelo de reglas, las correcciones del proxy bajo carga y con respuestas DNS cambiantes, las descargas de clientes VPN y la ISO de instalación.'),
 ('2026-10-07 a 13', 'De 26.1.0 a 26.1.2', 'Tudo o que havia na 26.1.1 (página de bloqueio, filtro de conteúdo, cliente do sandbox, Threat Analytics e Traffic Analytics, painel e gráficos novos, abas do Visualizador de logs, WAN padrão) e o trabalho da semana após os testes de laboratório: as paradas do motor encontradas e corrigidas, a interface 3.0, o novo modelo de regras, as correções do proxy sob carga e com respostas DNS que mudam, os downloads dos clientes VPN e a ISO de instalação.'))


# ---------------------------------------------------------------- performance and recovery (own section of the notes)
PERF = {
 'en': {
  'title': 'Performance and recovery',
  'intro': 'This section says what the lab tests of this release showed and how the firewall recovers by itself when its traffic engine stops answering. The numbers come from one small virtual machine and are meant to show how the protections add up, not to promise a throughput: size your firewall with the guidance at the end.',
  'setup_title': 'The lab and the method',
  'setup': [
   'Firewall: virtual machine with 4 processor cores and 4 GB of memory, Application Control, Network Protection (IPS), Web Protection with the antivirus, and the inspection of encrypted traffic, with the category lists loaded.',
   'Load: a client behind the firewall and a server on its internet side. Four parallel iperf3 streams (throughput), 100 new HTTP connections per second through the web proxy and 50 new HTTPS connections per second, all at once, for 60 seconds per configuration.',
   'A connection counts as completed when the whole answer arrived within 3 seconds (8 seconds for HTTPS).',
  ],
  'results_title': 'Results',
  'table': {'headers': ['Configuration', 'Throughput', 'HTTP completed', 'HTTPS completed'], 'rows': [
   ['Everything off (reference)', '1.48 Gbps', '99 %', '99 %'],
   ['Application Control only', '1.99 Gbps', '72 %', '48 %'],
   ['Application Control and IPS', '1.64 Gbps', '46 %', '84 %'],
   ['Plus the web proxy, no inspection', '1.33 Gbps', '30 %', '74 %'],
   ['Plus inspection of encrypted traffic', '1.22 Gbps', '43 %', '69 %'],
   ['Everything on, all rules on, category lists loaded', '1.22 Gbps', '97 %', '99 %'],
   ['5 minutes, everything on (final code), load average 16 to 18', '780 Mbps', 'most failed', '78 %'],
   ['Web proxy alone, 100 HTTP connections per second', 'not measured', '90 %', 'not measured'],
  ]},
  'reading': [
   'The firewall was limited by its processor (system time above 90 % in the long test), not by memory or by the engine standing still: the more protections are on, the lower the throughput and the fewer new connections complete while the line is full.',
   'The rows are not independent measurements: the machine and the test servers degraded after about an hour of repeated runs, so the order of the table is not a ranking of the features. Take them as indicative.',
   'At the load of the long test the web proxy could no longer answer most HTTP connections within 3 seconds. A firewall that must carry 1 Gbps and open hundreds of connections per second with all protections on needs more than 4 cores.',
  ],
  'recovery_title': 'How the firewall recovers by itself',
  'recovery_intro': 'The traffic engine (Application Control) and the intrusion prevention engine read the packets that the firewall hands to them. If a reader stops answering, new connections that it was asked to look at hang while others keep working. A watchdog finds this and fixes it without anyone logging in:',
  'recovery_steps': [
   'Every minute it takes three samples of each engine queue, 10 seconds apart.',
   'A queue is stalled when packets wait in all three samples and either its verdict counter did not move, or at least 64 packets wait and fewer than 10 verdicts per second are given. A reader that keeps up but is busy because the machine is overloaded is not restarted, because a restart would cost more than it gives.',
   'On a stall it saves a report (queue state, memory, processes; the newest 10 are kept in /root/nfq-stall) and, at once, takes the engine\'s queue rules out of the path, so traffic flows without analysis until the engine is back. With the "block" overload choice, and for the IPS, the rules are left alone.',
   'It then restarts the engine that owns the stalled queue. Limits: at most 6 restarts an hour and a pause of 90 seconds between two; over the limit it only reports.',
   'It records the event in the log (tag nexwall-nfq-watchdog), raises an alert (Status center, Dashboard) and writes a metric. The engine puts its rules back when it starts again.',
  ],
  'limits_title': 'Other protections that fail open',
  'limits': [
   'When the engine cannot keep up the default is to let traffic through (setting "when the engine is overloaded" in Application Control), not to block it.',
   'If the web proxy stops answering, the guard removes the redirect and web traffic flows without inspection until the proxy is back.',
   'If the antivirus engine is down the files are delivered unscanned (fail open) and the pages and the Dashboard show the antivirus as not running.',
   'Settings are in /etc/config/netifyd (section watchdog): enabled, restart, max_restarts, backlog, min_rate, failsafe and core (a core dump of a stalled engine for analysis).',
   'Sizing: 2 GB of memory is the least; use 8 GB when the antivirus, the inspection, the IPS and Application Control all run on a busy network. On 4 GB the system can stop the antivirus engine under heavy load.',
  ],
 },
 'es': {
  'title': 'Rendimiento y recuperación',
  'intro': 'Esta sección dice lo que mostraron las pruebas de laboratorio de esta versión y cómo se recupera el firewall por sí solo cuando su motor de tráfico deja de responder. Las cifras vienen de una máquina virtual pequeña y sirven para mostrar cómo se suman las protecciones, no para prometer un caudal: dimensione su firewall con la guía del final.',
  'setup_title': 'El laboratorio y el método',
  'setup': [
   'Firewall: máquina virtual con 4 núcleos y 4 GB de memoria, Control de aplicaciones, Protección de red (IPS), Web Protection con el antivirus y la inspección del tráfico cifrado, con las listas de categorías cargadas.',
   'Carga: un cliente detrás del firewall y un servidor del lado de internet. Cuatro flujos iperf3 en paralelo (caudal), 100 conexiones HTTP nuevas por segundo por el proxy web y 50 conexiones HTTPS nuevas por segundo, todo a la vez, durante 60 segundos por configuración.',
   'Una conexión cuenta como completada cuando la respuesta entera llegó en 3 segundos (8 segundos en HTTPS).',
  ],
  'results_title': 'Resultados',
  'table': {'headers': ['Configuración', 'Caudal', 'HTTP completadas', 'HTTPS completadas'], 'rows': [
   ['Todo apagado (referencia)', '1,48 Gbps', '99 %', '99 %'],
   ['Solo Control de aplicaciones', '1,99 Gbps', '72 %', '48 %'],
   ['Control de aplicaciones e IPS', '1,64 Gbps', '46 %', '84 %'],
   ['Más el proxy web, sin inspección', '1,33 Gbps', '30 %', '74 %'],
   ['Más inspección del tráfico cifrado', '1,22 Gbps', '43 %', '69 %'],
   ['Todo activado, todas las reglas, listas de categorías cargadas', '1,22 Gbps', '97 %', '99 %'],
   ['5 minutos, todo activado (código final), carga media de 16 a 18', '780 Mbps', 'la mayoría falló', '78 %'],
   ['Proxy web solo, 100 conexiones HTTP por segundo', 'no medido', '90 %', 'no medido'],
  ]},
  'reading': [
   'El límite del firewall fue su procesador (tiempo de sistema por encima del 90 % en la prueba larga), no la memoria ni que el motor se detuviera: cuantas más protecciones están activas, menor el caudal y menos conexiones nuevas se completan con la línea llena.',
   'Las filas no son mediciones independientes: la máquina y los servidores de prueba se degradaron tras cerca de una hora de ejecuciones repetidas, así que el orden de la tabla no es una clasificación de las funciones. Tómelas como indicativas.',
   'Con la carga de la prueba larga el proxy web ya no pudo responder la mayoría de las conexiones HTTP en 3 segundos. Un firewall que deba llevar 1 Gbps y abrir cientos de conexiones por segundo con todas las protecciones necesita más de 4 núcleos.',
  ],
  'recovery_title': 'Cómo se recupera el firewall por sí solo',
  'recovery_intro': 'El motor de tráfico (Control de aplicaciones) y el motor de prevención de intrusiones leen los paquetes que el firewall les entrega. Si un lector deja de responder, las conexiones nuevas que debía mirar se cuelgan mientras las demás siguen funcionando. Un vigilante lo detecta y lo corrige sin que nadie inicie sesión:',
  'recovery_steps': [
   'Cada minuto toma tres muestras de cada cola del motor, con 10 segundos de diferencia.',
   'Una cola está detenida cuando hay paquetes esperando en las tres muestras y su contador de veredictos no se movió, o hay al menos 64 paquetes esperando y se dan menos de 10 veredictos por segundo. Un lector que sigue el ritmo pero está ocupado porque la máquina está sobrecargada no se reinicia, porque el reinicio costaría más de lo que aporta.',
   'Ante una detención guarda un informe (estado de las colas, memoria, procesos; se conservan los 10 más recientes en /root/nfq-stall) y, de inmediato, saca del camino las reglas de cola del motor, de modo que el tráfico fluye sin análisis hasta que el motor vuelve. Con la opción de sobrecarga "bloquear", y para el IPS, las reglas no se tocan.',
   'Luego reinicia el motor dueño de la cola detenida. Límites: como máximo 6 reinicios por hora y una pausa de 90 segundos entre dos; pasado el límite solo informa.',
   'Registra el evento en el registro (etiqueta nexwall-nfq-watchdog), genera una alerta (Centro de estado, Panel) y escribe una métrica. El motor repone sus reglas al arrancar de nuevo.',
  ],
  'limits_title': 'Otras protecciones que fallan abiertas',
  'limits': [
   'Cuando el motor no da abasto, lo predeterminado es dejar pasar el tráfico (ajuste "cuando el motor está sobrecargado" en Control de aplicaciones), no bloquearlo.',
   'Si el proxy web deja de responder, el guardián quita la redirección y el tráfico web fluye sin inspección hasta que el proxy vuelve.',
   'Si el motor del antivirus está caído, los archivos se entregan sin analizar (falla abierto) y las páginas y el Panel muestran el antivirus como detenido.',
   'Los ajustes están en /etc/config/netifyd (sección watchdog): enabled, restart, max_restarts, backlog, min_rate, failsafe y core (un volcado de memoria del motor detenido para análisis).',
   'Dimensionamiento: 2 GB de memoria es lo mínimo; use 8 GB cuando el antivirus, la inspección, el IPS y el Control de aplicaciones funcionan juntos en una red con mucho tráfico. Con 4 GB el sistema puede detener el motor del antivirus bajo carga fuerte.',
  ],
 },
 'pt-BR': {
  'title': 'Desempenho e recuperação',
  'intro': 'Esta seção diz o que os testes de laboratório desta versão mostraram e como o firewall se recupera sozinho quando seu motor de tráfego deixa de responder. Os números vêm de uma máquina virtual pequena e servem para mostrar como as proteções se somam, não para prometer uma vazão: dimensione seu firewall com a orientação do final.',
  'setup_title': 'O laboratório e o método',
  'setup': [
   'Firewall: máquina virtual com 4 núcleos e 4 GB de memória, Controle de aplicações, Proteção de rede (IPS), Web Protection com o antivírus e a inspeção do tráfego criptografado, com as listas de categorias carregadas.',
   'Carga: um cliente atrás do firewall e um servidor do lado da internet. Quatro fluxos iperf3 em paralelo (vazão), 100 conexões HTTP novas por segundo pelo proxy web e 50 conexões HTTPS novas por segundo, tudo ao mesmo tempo, por 60 segundos em cada configuração.',
   'Uma conexão conta como concluída quando a resposta inteira chegou em 3 segundos (8 segundos no HTTPS).',
  ],
  'results_title': 'Resultados',
  'table': {'headers': ['Configuração', 'Vazão', 'HTTP concluídas', 'HTTPS concluídas'], 'rows': [
   ['Tudo desligado (referência)', '1,48 Gbps', '99 %', '99 %'],
   ['Só Controle de aplicações', '1,99 Gbps', '72 %', '48 %'],
   ['Controle de aplicações e IPS', '1,64 Gbps', '46 %', '84 %'],
   ['Mais o proxy web, sem inspeção', '1,33 Gbps', '30 %', '74 %'],
   ['Mais inspeção do tráfego criptografado', '1,22 Gbps', '43 %', '69 %'],
   ['Tudo ligado, todas as regras, listas de categorias carregadas', '1,22 Gbps', '97 %', '99 %'],
   ['5 minutos, tudo ligado (código final), carga média de 16 a 18', '780 Mbps', 'a maioria falhou', '78 %'],
   ['Proxy web sozinho, 100 conexões HTTP por segundo', 'não medido', '90 %', 'não medido'],
  ]},
  'reading': [
   'O limite do firewall foi o processador (tempo de sistema acima de 90 % no teste longo), não a memória nem o motor parar: quanto mais proteções ligadas, menor a vazão e menos conexões novas se completam com a linha cheia.',
   'As linhas não são medições independentes: a máquina e os servidores de teste se degradaram após cerca de uma hora de execuções repetidas, então a ordem da tabela não é um ranking dos recursos. Considere-as indicativas.',
   'Com a carga do teste longo o proxy web não conseguiu mais responder a maioria das conexões HTTP em 3 segundos. Um firewall que precise levar 1 Gbps e abrir centenas de conexões por segundo com todas as proteções precisa de mais de 4 núcleos.',
  ],
  'recovery_title': 'Como o firewall se recupera sozinho',
  'recovery_intro': 'O motor de tráfego (Controle de aplicações) e o motor de prevenção de intrusões leem os pacotes que o firewall entrega a eles. Se um leitor deixa de responder, as conexões novas que ele devia olhar travam enquanto as outras continuam funcionando. Um vigia percebe e corrige sem que ninguém entre no equipamento:',
  'recovery_steps': [
   'A cada minuto ele colhe três amostras de cada fila do motor, com 10 segundos de intervalo.',
   'Uma fila está parada quando há pacotes esperando nas três amostras e o contador de veredictos não se moveu, ou há pelo menos 64 pacotes esperando e menos de 10 veredictos por segundo são dados. Um leitor que acompanha o ritmo mas está ocupado porque a máquina está sobrecarregada não é reiniciado, porque o reinício custaria mais do que traz.',
   'Numa parada ele salva um relatório (estado das filas, memória, processos; os 10 mais recentes ficam em /root/nfq-stall) e, na hora, tira do caminho as regras de fila do motor, de modo que o tráfego flui sem análise até o motor voltar. Com a opção de sobrecarga "bloquear", e para o IPS, as regras não são mexidas.',
   'Depois reinicia o motor dono da fila parada. Limites: no máximo 6 reinícios por hora e uma pausa de 90 segundos entre dois; acima do limite ele só informa.',
   'Registra o evento no log (etiqueta nexwall-nfq-watchdog), gera um alerta (Central de status, Painel) e escreve uma métrica. O motor repõe as regras ao iniciar de novo.',
  ],
  'limits_title': 'Outras proteções que falham abertas',
  'limits': [
   'Quando o motor não dá conta, o padrão é deixar o tráfego passar (opção "quando o motor está sobrecarregado" no Controle de aplicações), não bloquear.',
   'Se o proxy web deixa de responder, o guardião remove o redirecionamento e o tráfego web flui sem inspeção até o proxy voltar.',
   'Se o motor do antivírus está parado, os arquivos são entregues sem varredura (falha aberta) e as páginas e o Painel mostram o antivírus como parado.',
   'As opções estão em /etc/config/netifyd (seção watchdog): enabled, restart, max_restarts, backlog, min_rate, failsafe e core (um despejo de memória do motor parado para análise).',
   'Dimensionamento: 2 GB de memória é o mínimo; use 8 GB quando o antivírus, a inspeção, o IPS e o Controle de aplicações funcionam juntos numa rede com muito tráfego. Com 4 GB o sistema pode parar o motor do antivírus sob carga pesada.',
  ],
 },
}

for _l,(_tt,_tl,_nt,_nl) in {'en': ('What was tested', ['Stress and soak: the load above in eight configurations, one 5 minute soak with everything on and a rate ramp up to 1,500 new connections per second against the firewall.', 'Recovery: the watchdog was tested with 31 automatic cases (frozen counter, slow backlog, fast backlog that is only load, cooldown, hourly limit, failsafe) and met in the lab five times under load (before the speed rule was added; a 5 minute soak at load 16 to 18 afterwards caused no restart); each time it took the engine out of the path and restarted it, and traffic kept flowing.', 'Web Protection, on a real client: block page on HTTPS and HTTP, SafeSearch for Google, Bing and DuckDuckGo, YouTube restricted mode, content filter (a normal page passes, an adult page is blocked), antivirus (an EICAR test file is blocked, a clean file passes), inspection with the firewall certificate, QUIC refusal, and connections to sites whose DNS answers differ.', 'Logging: every event above reached the Log Viewer (Firewall traffic, Application Control, Web Protection, system).'], 'Not tested', ['Intrusion detection with real attack signatures (the probes sent did not raise alerts, so the IPS alert path was not exercised in this round).', 'Runs longer than 5 minutes, hardware appliances, and more than one client at a time.', 'The installer ISO was started in UEFI and reached its language menu; installing to a disk from this exact build is checked separately.']), 'es': ('Qué se probó', ['Estrés y resistencia: la carga anterior en ocho configuraciones, una prueba de 5 minutos con todo activado y una rampa de hasta 1.500 conexiones nuevas por segundo contra el firewall.', 'Recuperación: el vigilante se probó con 31 casos automáticos (contador congelado, cola lenta, cola rápida que solo es carga, pausa, límite por hora, salida de emergencia) y se encontró cinco veces en el laboratorio bajo carga (antes de añadir la regla de velocidad; una prueba de 5 minutos con carga de 16 a 18 después no causó reinicios); cada vez sacó el motor del camino y lo reinició, y el tráfico siguió fluyendo.', 'Web Protection, en un cliente real: página de bloqueo en HTTPS y HTTP, SafeSearch de Google, Bing y DuckDuckGo, modo restringido de YouTube, filtro de contenido (una página normal pasa, una para adultos se bloquea), antivirus (un archivo de prueba EICAR se bloquea, uno limpio pasa), inspección con el certificado del firewall, rechazo de QUIC y conexiones a sitios cuyas respuestas DNS difieren.', 'Registros: cada evento anterior llegó al Visor de registros (Tráfico del firewall, Control de aplicaciones, Web Protection, sistema).'], 'No se probó', ['Detección de intrusiones con firmas de ataque reales (las pruebas enviadas no generaron alertas, así que la ruta de alertas del IPS no se ejerció en esta ronda).', 'Ejecuciones de más de 5 minutos, equipos físicos y más de un cliente a la vez.', 'La ISO de instalación se inició en UEFI y llegó a su menú de idioma; la instalación en un disco con esta compilación exacta se comprueba aparte.']), 'pt-BR': ('O que foi testado', ['Estresse e resistência: a carga acima em oito configurações, um teste de 5 minutos com tudo ligado e uma rampa de até 1.500 conexões novas por segundo contra o firewall.', 'Recuperação: o vigia foi testado com 31 casos automáticos (contador congelado, fila lenta, fila rápida que é só carga, pausa, limite por hora, saída de emergência) e foi acionado cinco vezes no laboratório sob carga (antes de acrescentar a regra de velocidade; um teste de 5 minutos com carga de 16 a 18 depois não causou reinício); cada vez tirou o motor do caminho e o reiniciou, e o tráfego continuou fluindo.', 'Web Protection, em um cliente real: página de bloqueio em HTTPS e HTTP, SafeSearch do Google, Bing e DuckDuckGo, modo restrito do YouTube, filtro de conteúdo (uma página normal passa, uma adulta é bloqueada), antivírus (um arquivo de teste EICAR é bloqueado, um limpo passa), inspeção com o certificado do firewall, recusa do QUIC e conexões a sites cujas respostas DNS diferem.', 'Logs: cada evento acima chegou ao Visualizador de logs (Tráfego do firewall, Controle de aplicações, Web Protection, sistema).'], 'Não foi testado', ['Detecção de intrusões com assinaturas de ataque reais (as sondagens enviadas não geraram alertas, então o caminho de alertas do IPS não foi exercitado nesta rodada).', 'Execuções com mais de 5 minutos, equipamentos físicos e mais de um cliente ao mesmo tempo.', 'A ISO de instalação foi iniciada em UEFI e chegou ao menu de idioma; a instalação em disco com esta versão exata é verificada à parte.'])}.items():
    PERF[_l]['tested_title'] = _tt; PERF[_l]['tested'] = _tl; PERF[_l]['not_tested_title'] = _nt; PERF[_l]['not_tested'] = _nl

# ---------------------------------------------------------------- build the three files
for lang in L:
    d = copy.deepcopy(json.load(open('/root/rel-draft/26.1.1/%s.json' % lang)))
    d['title'] = 'Nexwall Firewall 26.1.2'
    d['summary'] = SUMMARY[lang]
    d['overview'] = OVERVIEW[lang]
    for row in d['at_a_glance']:
        if row['value'] == '26.1.1':
            row['value'] = '26.1.2'
        elif row is d['at_a_glance'][1]:
            row['value'] = STATUS[lang]
    old = {s['id']: s for s in d['sections']}
    new_items = {}
    for it in old['whats-new']['items']:
        new_items[it['title']] = it
    items = []
    base_titles = [it['title'] for it in old['whats-new']['items']]
    # the 26.1.1 items stay, in their order; the interface item is replaced by 3.0 and the new ones follow it
    for it in old['whats-new']['items']:
        if it['title'].lower().startswith(('a redesigned interface', 'una interfaz rediseñada', 'uma interface redesenhada')):
            items.append({'tag': 'new', 'title': DASHBOARD[lang][0], 'body': DASHBOARD[lang][1]})
            for k in ('rule_model', 'quic', 'badges', 'vpn_clients'):
                items.append({'tag': 'new', 'title': NEW[k][lang][0], 'body': NEW[k][lang][1]})
        else:
            items.append(it)
    old['whats-new']['items'] = items
    imp = [{'tag': 'improved', 'title': IMPROVED[k][lang][0], 'body': IMPROVED[k][lang][1]} for k in ('stall', 'conflict', 'wanlog', 'icmp', 'proxyload', 'wg', 'dpi')]
    imp += old['improvements']['items']
    old['improvements']['items'] = imp
    d['sections'] = [old['whats-new'], old['improvements']] + [s for s in d['sections'] if s['id'] not in ('whats-new', 'improvements')]
    rows = d['components']['rows']
    en_names = [r['name'] for r in json.load(open('/root/rel-draft/26.1.1/en.json'))['components']['rows']]
    for idx, en_name in enumerate(en_names):
        if en_name == 'Image':
            rows[idx]['version'] = '26.1.2'
        elif en_name == 'Firmware sources':
            rows[idx]['version'] = DATA.get('firmware_commit', 'main (set when the image is built)')
        elif en_name in COMPONENTS:
            version, note = COMPONENTS[en_name]
            rows[idx]['version'] = version
            if note:
                rows[idx]['note'] = note[lang]
        elif en_name == 'Traffic engine plugins':
            pass
    d['requirements'][2] = MEM[lang]
    d['timeline']['entries'] = [{'date': TIMELINE[lang][0], 'title': TIMELINE[lang][1], 'text': TIMELINE[lang][2]}]
    d['performance'] = PERF[lang]
    os.makedirs('content/26.1.2', exist_ok=True)
    json.dump(d, open('content/26.1.2/%s.json' % lang, 'w'), ensure_ascii=False, indent=2)
    open('content/26.1.2/%s.json' % lang, 'a').write('\n')

# ---------------------------------------------------------------- issues
reg = json.load(open('content/issues.json'))
have = {x['id'] for x in reg['issues']}
FIXED = [
 ('NXW-1030', 'engine', t('The traffic engine could stand still under load', 'El motor de tráfico podía detenerse con carga', 'O motor de tráfego podia travar sob carga'),
  t('Two threads of the Nexwall plugins waited for each other, and the capture thread ended when the kernel dropped a queued packet. Both are fixed and a watchdog recovers the engine if it ever stands still.', 'Dos hilos de los plugins de Nexwall se esperaban entre sí, y el hilo de captura terminaba cuando el kernel descartaba un paquete en cola. Ambos están corregidos y un vigilante recupera el motor si alguna vez se detiene.', 'Duas threads dos plugins da Nexwall esperavam uma pela outra, e a thread de captura terminava quando o kernel descartava um pacote da fila. As duas estão corrigidas e um vigia recupera o motor se ele alguma vez parar.')),
 ('NXW-1031', 'web-protection', t('Some sites did not open behind the web proxy (error 409)', 'Algunos sitios no se abrían detrás del proxy web (error 409)', 'Alguns sites não abriam atrás do proxy web (erro 409)'),
  t('Sites whose DNS answers differ between the client and the proxy were refused by the proxy. They now open: the connection goes to the address the client chose.', 'Los sitios cuyas respuestas DNS difieren entre el cliente y el proxy eran rechazados por el proxy. Ahora se abren: la conexión va a la dirección que eligió el cliente.', 'Os sites cujas respostas DNS diferem entre o cliente e o proxy eram recusados pelo proxy. Agora abrem: a conexão vai ao endereço que o cliente escolheu.')),
 ('NXW-1032', 'logging', t('The Firewall traffic tab showed only allowed traffic', 'La pestaña Tráfico del firewall solo mostraba tráfico permitido', 'A aba Tráfego do firewall mostrava só tráfego permitido'),
  t('What the WAN rejected was not logged. The WAN zone now logs it, at most 10 lines a minute.', 'Lo que rechazaba la WAN no se registraba. La zona WAN ahora lo registra, como máximo 10 líneas por minuto.', 'O que a WAN recusava não era registrado. A zona WAN agora registra, no máximo 10 linhas por minuto.')),
 ('NXW-1033', 'networking', t('A refused connection gave no answer to the client', 'Una conexión rechazada no daba respuesta al cliente', 'Uma conexão recusada não dava resposta ao cliente'),
  t('The traffic engine queue swallowed the ICMP "port unreachable" of a rejected connection and the messages of path MTU discovery. They pass now.', 'La cola del motor de tráfico absorbía el ICMP "puerto inalcanzable" de una conexión rechazada y los mensajes del descubrimiento de MTU. Ahora pasan.', 'A fila do motor de tráfego engolia o ICMP "porta inalcançável" de uma conexão recusada e as mensagens da descoberta de MTU. Agora passam.')),
 ('NXW-1034', 'web-protection', t('The web proxy could run out of open files and the antivirus switch off under load', 'El proxy web podía quedarse sin archivos abiertos y el antivirus apagarse con carga', 'O proxy web podia ficar sem arquivos abertos e o antivírus desligar sob carga'),
  t('The limit of open files is now 16,384, up to 256 files are scanned at once and the scanner connection is retried after 10 seconds.', 'El límite de archivos abiertos ahora es 16.384, se analizan hasta 256 archivos a la vez y la conexión del analizador se reintenta a los 10 segundos.', 'O limite de arquivos abertos agora é 16.384, até 256 arquivos são varridos ao mesmo tempo e a conexão do verificador é tentada de novo após 10 segundos.')),
 ('NXW-1035', 'networking', t('A WireGuard tunnel could pin its route to the wrong internet link', 'Un túnel WireGuard podía fijar su ruta al enlace de internet equivocado', 'Um túnel WireGuard podia fixar a rota no link de internet errado'),
  t('On a firewall with two internet links the route to the peer stayed on the link that was the default when the tunnel came up, which could cut the license and the updates. Tunnels no longer pin it.', 'En un firewall con dos enlaces de internet la ruta hacia el par se quedaba en el enlace que era el predeterminado cuando el túnel se levantó, lo que podía cortar la licencia y las actualizaciones. Los túneles ya no la fijan.', 'Em um firewall com dois links de internet a rota para o par ficava no link que era o padrão quando o túnel subiu, o que podia cortar a licença e as atualizações. Os túneis não a fixam mais.')),
 ('NXW-1036', 'interface', t('A page with several explanations could freeze the browser', 'Una página con varias explicaciones podía congelar el navegador', 'Uma página com várias explicações podia travar o navegador'),
  t('The explanation of each tab updated the shared description in a loop. Fixed in interface 3.0.', 'La explicación de cada pestaña actualizaba la descripción compartida en un bucle. Corregido en la interfaz 3.0.', 'A explicação de cada aba atualizava a descrição compartilhada em um laço. Corrigido na interface 3.0.')),
 ('NXW-1037', 'interface', t('Opening the unit chip made it disappear', 'Abrir el chip de la unidad lo hacía desaparecer', 'Abrir o chip da unidade fazia ele sumir'),
  t('The panel read the system information in the wrong shape and failed. Fixed.', 'El panel leía la información del sistema en la forma equivocada y fallaba. Corregido.', 'O painel lia as informações do sistema na forma errada e falhava. Corrigido.')),
]
KNOWN = [
 ('NXW-2016', 'web-protection', t('A blocked category is enforced by name only for connections the engine can read', 'Una categoría bloqueada se aplica por nombre solo en las conexiones que el motor puede leer', 'Uma categoria bloqueada é aplicada pelo nome só nas conexões que o motor consegue ler'),
  t('A device that connects to an address it resolved elsewhere (its own DNS over HTTPS, a hard-coded address) can reach a site of a blocked category when the name is not visible: the blocking by DNS does not apply to it.', 'Un dispositivo que se conecta a una dirección resuelta en otro lugar (su propio DNS sobre HTTPS, una dirección fija) puede llegar a un sitio de una categoría bloqueada cuando el nombre no es visible: el bloqueo por DNS no se aplica.', 'Um dispositivo que conecta a um endereço resolvido em outro lugar (o próprio DNS sobre HTTPS, um endereço fixo) pode chegar a um site de uma categoria bloqueada quando o nome não está visível: o bloqueio por DNS não se aplica.'),
  t('Block DNS over HTTPS (category "Encrypted DNS") and make the clients use the firewall for DNS.', 'Bloquee DNS sobre HTTPS (categoría "DNS cifrado") y haga que los clientes usen el firewall para DNS.', 'Bloqueie o DNS sobre HTTPS (categoria "DNS criptografado") e faça os clientes usarem o firewall para DNS.')),
 ('NXW-2017', 'system', t('Tight memory on 4 GB with everything running', 'Memoria justa con 4 GB con todo en ejecución', 'Memória apertada com 4 GB com tudo em execução'),
  t('With the antivirus, the inspection, the intrusion prevention and Application Control on a busy network, a 4 GB system uses its swap and the system can stop the antivirus engine for a while. The antivirus fails open and the Dashboard shows it as not running.', 'Con el antivirus, la inspección, la prevención de intrusiones y el Control de aplicaciones en una red con mucho tráfico, un sistema de 4 GB usa su swap y el sistema puede detener el motor del antivirus durante un tiempo. El antivirus falla abierto y el Panel lo muestra como detenido.', 'Com o antivírus, a inspeção, a prevenção de intrusões e o Controle de aplicações em uma rede com muito tráfego, um sistema de 4 GB usa o swap e o sistema pode parar o motor do antivírus por um tempo. O antivírus falha aberto e o Painel o mostra como parado.'),
  t('Give the firewall 8 GB when all the protections run on a busy network.', 'Dé 8 GB al firewall cuando todas las protecciones funcionan en una red con mucho tráfico.', 'Dê 8 GB ao firewall quando todas as proteções funcionam em uma rede com muito tráfego.')),
]
for iid, area, title, body in FIXED:
    if iid not in have:
        reg['issues'].append({'id': iid, 'type': 'fixed', 'version': '26.1.2', 'area': area, 'title': title, 'body': body})
for iid, area, title, body, work in KNOWN:
    if iid not in have:
        reg['issues'].append({'id': iid, 'type': 'known', 'introduced': '26.1.2', 'fixed': None, 'area': area, 'title': title, 'body': body, 'workaround': work})
json.dump(reg, open('content/issues.json', 'w'), ensure_ascii=False, indent=1)
open('content/issues.json', 'a').write('\n')

# ---------------------------------------------------------------- the release list (only with --publish: needs the real files)
if '--publish' in sys.argv:
    rel = json.load(open('content/releases.json'))
    rel = [r for r in rel if r['version'] != '26.1.2']
    rel.insert(0, {'version': '26.1.2', 'date': DATA['date'], 'status': 'stable', 'downloads': DATA['downloads']})
    json.dump(rel, open('content/releases.json', 'w'), ensure_ascii=False, indent=1)
    open('content/releases.json', 'a').write('\n')
print('26.1.2 written; issues:', len(reg['issues']))
