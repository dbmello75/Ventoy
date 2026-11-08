# Integração dos PRs abertos de ventoy/Ventoy

Foram considerados os 117 PRs abertos capturados no início desta integração.
O inventário em [open-prs.json](open-prs.json) registra o SHA exato de cada contribuição,
o ancestral usado para o diff, os arquivos alterados e a decisão individual.

Resultado: **111 PRs incorporados ou adaptados, 4 já presentes/substituídos e 2 descartados**.
Os descartados são #2347 (arquivo de treinamento) e #2524 (log pessoal).
A incorporação registra a origem dos PRs no histórico; adaptações podem diferir do patch original.
Não foram criadas revisões, comentários nem fechamentos no repositório upstream.

## Validação realizada

- 36 arquivos JSON e 54 idiomas GUI, com chaves JSON duplicadas rejeitadas.
- 3.030 combinações de buffers/escapes JSON, incluindo UTF-8, tamanhos zero/negativos e guardas de memória.
- ASan e UBSan aprovados. LeakSanitizer foi desativado localmente porque o ambiente executa sob ptrace.
- Parser de locales Plugson testado com formato legado, sat_IN, limites de capacidade e entrada nula.
- Validador JSON nativo do Ventoy e verificador de ordenação/UTF-8 aprovados.
- JavaScript, YAML dos workflows e Python das ferramentas de teste verificados.
- 288 scripts shell completos passaram pela checagem de sintaxe. O fragmento de injeção
  `IMG/cpio/ventoy/hook/alpine/insert.sh` já era incompleto isoladamente na base.
- VtoyTool compilado em x86_64; ajuda de vtoydm executada. O compilador ainda emite avisos existentes.
- Fontes nativas de disco/utilitários da GUI Linux e servidor Web Plugson passaram por gcc -fsyntax-only.
- Falta de uma release compilada é tratada como erro pela geração de USB virtual, sem criar imagem vazia.

## Limites e recursos experimentais

Não há Docker, QEMU, MSVC, dependências GTK/UDisks2 nem toolchain LoongArch disponíveis
neste ambiente. Não foram feitos builds completos de release, prova de reprodutibilidade,
boot BIOS/UEFI, teste em Windows ou instalação em discos físicos.
Esta integração não é uma certificação de release e os testes locais não provam compatibilidade de firmware.

O backend Linux nativo continua padrão. A opção UDisks2/Flatpak é experimental;
o manifesto ainda usa payload upstream 1.1.05 e exige validação própria.
LoongArch é WIP e exige preparação da árvore EDK2 indicada pelo port e
`VTOY_BUILD_LOONGARCH=1`. Workflows de reprodutibilidade e matriz QEMU são manuais.
Eles não podem declarar boot aprovado apenas por capturar telas; exigem uma expressão
`VTOY_BOOT_SUCCESS_REGEX` que corresponda à saída serial do sistema convidado.
O instalador EFI do #3788 permanece uma [proposta](../Proposals/EFI-tool.md), sem código implementado.

## Reproduzir as verificações locais

```sh
python3 tests/integration/check.py
ASAN_OPTIONS=detect_leaks=0 VTOY_SANITIZE=1 python3 tests/integration/check.py
sh LANGUAGES/check.sh "$PWD"
bash LANGUAGES/languages_check_order.sh --check-utf8 LANGUAGES/languages.json
```

## Análise individual

| PR | Estado | Avaliação e resolução |
|---|---|---|
| [#33](https://github.com/ventoy/Ventoy/pull/33) — Replace hard-coded LocalDebuggerWorkingDirectory | Adaptado | Diretório de depuração substituído por $(OutDir) em todas as configurações atuais, preservando as plataformas adicionadas depois do PR. |
| [#414](https://github.com/ventoy/Ventoy/pull/414) — Update the compilation instructions to mention how to build with Docker | Adaptado | Instruções de Docker Compose adicionadas ao README atual, preservando a lista recente de sistemas e a documentação existente. |
| [#417](https://github.com/ventoy/Ventoy/pull/417) — Modernized Shell Script functions. | Adaptado | Corrigidos grep -e para grep -E e multiplicação POSIX sem escape no contexto aritmético; não foram aplicadas as regressões do patch original. |
| [#418](https://github.com/ventoy/Ventoy/pull/418) — Lossless compression | Adaptado | Compressão PNG incorporada, mantendo a modernização de shell corrigida pelo #417 e evitando substituir o ícone Ubuntu mais recente por uma versão antiga. |
| [#423](https://github.com/ventoy/Ventoy/pull/423) — Switch from wget to curl in Dockerfile and make sure archives are overwritten | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#424](https://github.com/ventoy/Ventoy/pull/424) — Add --help to CreatePersistentImg.sh | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#425](https://github.com/ventoy/Ventoy/pull/425) — Proposal: Do not prompt for confirmation when '-I' is set | Adaptado | Instalação forçada -I dispensa as duas confirmações; instalação normal mantém os avisos. Nenhum instalador foi executado em disco físico. |
| [#559](https://github.com/ventoy/Ventoy/pull/559) — Create ccpp.yml | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#841](https://github.com/ventoy/Ventoy/pull/841) — OS-Logo | Integrado | Conjunto de ícones de sistemas adicionado ao tema; estes são recursos visuais, não novos mecanismos de boot. |
| [#879](https://github.com/ventoy/Ventoy/pull/879) — Helper script for the build environment preparation | Adaptado | Helper de preparação mantido, atualizado para construir o ambiente Docker experimental do #3755 em vez de reinstalar toolchains antigos no host. |
| [#920](https://github.com/ventoy/Ventoy/pull/920) — Create .gitignore (to ignore macos .DS_Store files) | Integrado | Regra .DS_Store incorporada e combinada com as regras de build/IDE dos PRs posteriores. |
| [#1071](https://github.com/ventoy/Ventoy/pull/1071) — update | Já presente | O diff contra o ancestral comum é vazio; não há alteração adicional a incorporar. |
| [#1291](https://github.com/ventoy/Ventoy/pull/1291) — Use system native default font in GUI | Adaptado | Fonte padrão nativa Windows usada para Courier New; fontes específicas escolhidas pelas traduções são respeitadas. Arquivos UTF-16 preservados. |
| [#1468](https://github.com/ventoy/Ventoy/pull/1468) — modernize js | Adaptado | Modernização JavaScript incorporada; variáveis reatribuídas usam let, incluindo url, data, func, msg_class e $messageContainer. |
| [#1469](https://github.com/ventoy/Ventoy/pull/1469) — FreeNAS is TrueNAS Core and KolibriOS is no Linux | Adaptado | KolibriOS classificado em Other e referência FreeNAS redundante removida, sem voltar à lista antiga de distribuições. |
| [#1557](https://github.com/ventoy/Ventoy/pull/1557) — Re-write if-else block as switch-case block | Adaptado | Conversão para switch preserva também as opções r, w e C adicionadas desde a criação do PR. VtoyTool compilado em x86_64 e ajuda vtoydm exercitada. |
| [#1558](https://github.com/ventoy/Ventoy/pull/1558) — Add check on length of name. | Integrado | Guarda de comprimento incorporada antes do acesso aos caracteres do nome de dispositivo. |
| [#1559](https://github.com/ventoy/Ventoy/pull/1559) — Add length check on command line input | Integrado | Guarda de comprimento incorporada para o argumento do utilitário chmod. |
| [#1791](https://github.com/ventoy/Ventoy/pull/1791) — Update Russian translation & fix of couple things in Linux GUI | Adaptado | Textos russos reconciliados por chave. Ajustes de GUI originais foram preservados no backend nativo e no backend opcional quando aplicáveis. |
| [#1808](https://github.com/ventoy/Ventoy/pull/1808) — add allocation memory error processing for Ventoy2DiskInit | Adaptado | Falha de alocação retorna ERROR_NOT_ENOUGH_MEMORY; reinicialização de discos e entrada da GUI interrompem o fluxo. Tipos de retorno preservados. |
| [#2011](https://github.com/ventoy/Ventoy/pull/2011) — sorting languages by name | Adaptado | Ordenação aplicada ao conjunto final de traduções; não foi restaurado o arquivo antigo do PR. |
| [#2340](https://github.com/ventoy/Ventoy/pull/2340) — Updated Greek Language | Adaptado | Tradução grega reconciliada por chave sem substituir o catálogo atual por uma cópia antiga reformatada. |
| [#2347](https://github.com/ventoy/Ventoy/pull/2347) — added first text feature | Descartado | Adiciona somente text_feature com comentários de treinamento; não implementa recurso do Ventoy. |
| [#2352](https://github.com/ventoy/Ventoy/pull/2352) — Reduced the big paragraph to dropdown | Adaptado | Seções de sistemas testados tornadas recolhíveis, preservando todas as entradas atuais. |
| [#2399](https://github.com/ventoy/Ventoy/pull/2399) — Hide VTOYEFI partition by marking as `diag` | Integrado | VTOYEFI recebe flag diag no caminho GPT tratado pelo PR; compatibilidade de firmware exige teste de boot. |
| [#2420](https://github.com/ventoy/Ventoy/pull/2420) — Add tabindex=0 to HTML properties | Integrado | Tabindex incorporado aos controles WebUI indicados pelo PR. |
| [#2450](https://github.com/ventoy/Ventoy/pull/2450) — Update README.md | Adaptado | Melhorias de texto incorporadas com correção da frase gramaticalmente incorreta proposta para MBR/GPT. |
| [#2451](https://github.com/ventoy/Ventoy/pull/2451) — Update build.sh | Integrado | Comentários e estrutura do build de vtoygpt incorporados; não executado com os toolchains de todas as arquiteturas. |
| [#2466](https://github.com/ventoy/Ventoy/pull/2466) — Update theme.txt | Integrado | Configuração de alinhamento e escala da imagem de fundo incorporada ao tema. |
| [#2476](https://github.com/ventoy/Ventoy/pull/2476) — Add Brazilian Portuguese translation to menu/help, update language translation for new 4K string | Adaptado | pt-BR menu/help incorporados por chave e reconciliados com #3691/#3747; conteúdo recente preservado. |
| [#2489](https://github.com/ventoy/Ventoy/pull/2489) — Added Chinese Traditional to languages.json | Integrado | Contribuição zh-TW consolidada com a tradução existente; nomes alternativos não criam idiomas duplicados. |
| [#2524](https://github.com/ventoy/Ventoy/pull/2524) — Create log.txt | Descartado | Adiciona somente um log pessoal de execução com caminhos locais; não contém correção ou funcionalidade. |
| [#2619](https://github.com/ventoy/Ventoy/pull/2619) — Fix typo in README | Adaptado | Correção de texto incorporada ao README final. |
| [#2622](https://github.com/ventoy/Ventoy/pull/2622) — Update localboot.cfg to add exit | Integrado | Entrada para retornar ao firmware adicionada ao menu de boot local. Comportamento real depende do firmware. |
| [#2625](https://github.com/ventoy/Ventoy/pull/2625) — Bugfix VentoyWorker.sh - mount detection false-positive | Integrado | Pesquisa de montagem passa a usar correspondência de palavra para reduzir falsos positivos de nomes de disco. |
| [#2635](https://github.com/ventoy/Ventoy/pull/2635) — Use exfatprogs instead of exfat-utils to handle exFAT filesystem operations | Integrado | Seleção entre mkfs.exfat e mkexfatfs incorporada; argumentos específicos de cada ferramenta preservados. |
| [#2651](https://github.com/ventoy/Ventoy/pull/2651) — Fix selinux for vtoycow in CreatePersistentImg.sh | Integrado | Preparação de diretórios e contexto SELinux para vtoycow incorporada. Não executada em partições físicas. |
| [#2660](https://github.com/ventoy/Ventoy/pull/2660) — Solved passphrase error | Adaptado | Passphrase agora é argumento de printf com formato fixo %s; percentuais e hífens deixam de ser interpretados como formato/opção. |
| [#2681](https://github.com/ventoy/Ventoy/pull/2681) — Create he_HE | Integrado | Tradução hebraica mantida com JSON reparado e nome normalizado para he_IL.json. |
| [#2717](https://github.com/ventoy/Ventoy/pull/2717) — move ReviOS per issue #2716 | Adaptado | ReviOS movido para Windows; link inexistente revios,.md proposto pelo PR não foi criado. |
| [#2756](https://github.com/ventoy/Ventoy/pull/2756) — Update ar_AR.txt | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#2767](https://github.com/ventoy/Ventoy/pull/2767) — Update README.md | Adaptado | Introdução do README convertida em parágrafos sem restaurar dados antigos de compatibilidade. |
| [#2803](https://github.com/ventoy/Ventoy/pull/2803) — Fix English Translation | Adaptado | Revisões de inglês incorporadas ao catálogo e ao README atual. |
| [#2868](https://github.com/ventoy/Ventoy/pull/2868) — Update languages.json | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#2881](https://github.com/ventoy/Ventoy/pull/2881) — Update languages.json Japanese | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#2882](https://github.com/ventoy/Ventoy/pull/2882) — Update ko_KR.json | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#2886](https://github.com/ventoy/Ventoy/pull/2886) — Updated translation | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#2927](https://github.com/ventoy/Ventoy/pull/2927) — Update INSTALL menu/help Japanese | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#2931](https://github.com/ventoy/Ventoy/pull/2931) — Update sr_RS.txt | Adaptado | Sérvio reconciliado com as atualizações posteriores #3305/#3604/#3605, preservando as chaves novas. |
| [#2941](https://github.com/ventoy/Ventoy/pull/2941) — Added Norwegian Bokmål and Nynorsk translations | Integrado | Bokmål/Nynorsk incorporados e nomes nb-NO/nn-NO normalizados para nb_NO/nn_NO; chaves ausentes recebem fallback inglês. |
| [#2955](https://github.com/ventoy/Ventoy/pull/2955) — [WIP] Loongarch support | Adaptado | Port LoongArch WIP incorporado como experimental; EDK2 adicional exige VTOY_BUILD_LOONGARCH=1. Toolchain e hardware LoongArch não validados; arquivo .orig gerado removido. |
| [#2962](https://github.com/ventoy/Ventoy/pull/2962) — Add Estonian translation | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#2986](https://github.com/ventoy/Ventoy/pull/2986) — Improved Spanish Translations | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3000](https://github.com/ventoy/Ventoy/pull/3000) — Update Galician language | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3016](https://github.com/ventoy/Ventoy/pull/3016) — Create devcontainer.json | Integrado | Configuração de devcontainer incorporada; criação do container não exercitada neste ambiente. |
| [#3031](https://github.com/ventoy/Ventoy/pull/3031) — Added Irish language | Integrado | Irlandês incorporado, vírgula final JSON reparada e token obrigatório YES preservado na instrução de confirmação. |
| [#3129](https://github.com/ventoy/Ventoy/pull/3129) — Update Slovenian languages.json | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3135](https://github.com/ventoy/Ventoy/pull/3135) — Update translations | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3157](https://github.com/ventoy/Ventoy/pull/3157) — Update Portuguese (Portugal) translation | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3175](https://github.com/ventoy/Ventoy/pull/3175) — Clean up block device detection logic | Adaptado | Espera/detecção de dispositivos incorporada com partprobe limitado ao disco selecionado e erro propagado; suporte exfatprogs do #2635 preservado. |
| [#3183](https://github.com/ventoy/Ventoy/pull/3183) — Update languages.json | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3186](https://github.com/ventoy/Ventoy/pull/3186) — Added Norwegian translation for INSTALL/grub/help and INSTALL/grub/menu | Adaptado | Bokmål consolidado com #2941 sem arquivos de locale duplicados. |
| [#3189](https://github.com/ventoy/Ventoy/pull/3189) — updated all_in_one.sh with code needed to build VtoyTool and others | Integrado | Notas de preparação de ferramentas incorporadas ao script de build. |
| [#3190](https://github.com/ventoy/Ventoy/pull/3190) — Basic support for porteuX boot | Adaptado | Detecção de initrd e configuração Syslinux de porteuX incorporada sem retirar caminhos mais recentes do GRUB. |
| [#3208](https://github.com/ventoy/Ventoy/pull/3208) — fixes 2 gtk failed assertions in VentoyGUI.x86_64 | Adaptado | can_default adicionado aos widgets; requisito GTK2 preservado para não invalidar a versão GTK2 existente. |
| [#3222](https://github.com/ventoy/Ventoy/pull/3222) — Create SECURITY.md | Adaptado | Template com versões fictícias substituído por política específica deste fork, sem inventar garantia de suporte ou prazo de resposta. |
| [#3225](https://github.com/ventoy/Ventoy/pull/3225) — Create SECURITY.md | Adaptado | Template duplicado consolidado na mesma SECURITY.md específica do fork. |
| [#3227](https://github.com/ventoy/Ventoy/pull/3227) — Create SECURITY.md | Adaptado | Terceiro template consolidado na mesma SECURITY.md; versões fictícias removidas. |
| [#3229](https://github.com/ventoy/Ventoy/pull/3229) — Remove 7zip BLOBs | Substituído | A base já removeu os blobs 7-Zip e usa releases de ventoy/7zip com SHA-256. O PR contém wget malformado e apontaria para outro distribuidor. |
| [#3232](https://github.com/ventoy/Ventoy/pull/3232) — updated 7za.exe dependencies to latest version 24.09 | Substituído | Atualizaria para 7-Zip 24.09; a base já usa ventoy-7zip-2605. Não foi aplicado um downgrade nem foram reintroduzidos os blobs removidos. |
| [#3233](https://github.com/ventoy/Ventoy/pull/3233) — added .gitignore | Adaptado | Regras de gitignore combinadas com as dos outros PRs; erro /NSTALL corrigido. |
| [#3237](https://github.com/ventoy/Ventoy/pull/3237) — Update languages.json | Integrado | Tradução hebraica incorporada com reparo da linha JSON que mesclava duas chaves. |
| [#3240](https://github.com/ventoy/Ventoy/pull/3240) — updated musl cross make link in ./BUSYBOX/build.txt | Integrado | URL de documentação do toolchain musl atualizada. |
| [#3266](https://github.com/ventoy/Ventoy/pull/3266) — Check mkfs.vfat command | Integrado | Verificação de disponibilidade de mkfs.fat adicionada à checagem de ferramentas. |
| [#3305](https://github.com/ventoy/Ventoy/pull/3305) — Update Serbian translations | Adaptado | Atualização sérvia incorporada e reconciliada cronologicamente com os PRs mais recentes. |
| [#3316](https://github.com/ventoy/Ventoy/pull/3316) — Remove trailing whitespace recursively | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3319](https://github.com/ventoy/Ventoy/pull/3319) — Add Flatpak support using UDisks2 | Integrado | Port UDisks2/Flatpak incorporado como opção VTOY_USE_UDISKS; backend nativo e cross builds preservados. Corrigidos casamento de partições, ponteiros nulos e referências de FD. Manifest experimental usa o código deste checkout; ainda referencia payload upstream 1.1.05. |
| [#3330](https://github.com/ventoy/Ventoy/pull/3330) — Allow theme to change tip font | Integrado | Campo menu-tip-font e valor padrão incorporados ao carregador de temas e plugins. |
| [#3368](https://github.com/ventoy/Ventoy/pull/3368) — [3352] Add scripts to validate and sort languages.json alphabetically | Adaptado | Validadores/ordenadores de idiomas incorporados; CHECK_UTF-8 corrigido para CHECK_UTF8 e temporário criado junto ao arquivo de destino. |
| [#3391](https://github.com/ventoy/Ventoy/pull/3391) — Update README.md badge link | Integrado | Link do badge de Actions atualizado. |
| [#3397](https://github.com/ventoy/Ventoy/pull/3397) — A better fix for ventoy/vtoyboot#48 | Integrado | Offset VDI lido do cabeçalho em vez de fixo em 2 MiB; adicionados limites de payload e terminação do texto de diagnóstico. Boot VDI real não testado. |
| [#3454](https://github.com/ventoy/Ventoy/pull/3454) — Add supported languages list and link in root README.md | Integrado | Lista de idiomas regenerada a partir do conjunto final, distinguindo GUI, menus GRUB e ajuda. |
| [#3462](https://github.com/ventoy/Ventoy/pull/3462) — Update supported Linux distributions list in README | Integrado | Omarchy adicionado à lista de sistemas relatados no README. |
| [#3465](https://github.com/ventoy/Ventoy/pull/3465) — Update German translation in languages.json | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3483](https://github.com/ventoy/Ventoy/pull/3483) — chore: Update outdated GitHub Actions versions | Integrado | Atualização de Actions conciliada com #3568: checkout v6 e upload-artifact v7. |
| [#3493](https://github.com/ventoy/Ventoy/pull/3493) — Fix secure boot flag description in README | Adaptado | Descrição Secure Boot mantida correta: habilitado por padrão, -S desabilita e -s habilita explicitamente. |
| [#3500](https://github.com/ventoy/Ventoy/pull/3500) — Improve Plugson browser handling on Windows. | Integrado | Plugson Windows usa o navegador padrão. Não foi executado em Windows neste ambiente. |
| [#3533](https://github.com/ventoy/Ventoy/pull/3533) — Add filename to the "File checksum" label in the secondary menu | Integrado | Nome do arquivo incluído na entrada de checksum do menu secundário. |
| [#3547](https://github.com/ventoy/Ventoy/pull/3547) — fix: pin 1 unpinned action | Integrado | Action de espelhamento fixada no SHA imutável proposto; nenhum espelhamento externo foi executado. |
| [#3554](https://github.com/ventoy/Ventoy/pull/3554) — Update Dockerfile | Substituído | Dockerfile proposto contém continuação de linha e URL LLVM malformadas. A alternativa moderna foi incorporada pelo Dockerfile.reproducible do #3755, mantida experimental. |
| [#3556](https://github.com/ventoy/Ventoy/pull/3556) — i18n: Include tl_PH (Tagalog) Translation | Integrado | Tagalog incorporado com fallback para as chaves UEFI novas ausentes no patch antigo. |
| [#3558](https://github.com/ventoy/Ventoy/pull/3558) — fix memory leak | Integrado | Recursos liberados nos caminhos de falha de alocação em vtoykmod e nos utilitários GPT. |
| [#3560](https://github.com/ventoy/Ventoy/pull/3560) — Feature: Optional per-class backgrounds for custom themes | Integrado | Fundos por classe de menu incorporados, habilitados apenas quando o tema contém backgrounds/. Renderização GRUB real não testada. |
| [#3565](https://github.com/ventoy/Ventoy/pull/3565) — Update Traditional Chinese string | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3568](https://github.com/ventoy/Ventoy/pull/3568) — Bump GitHub Actions to fix Node.js 20 deprecation | Adaptado | upload-artifact v7 conciliado com checkout v6 no CI ativo e nas ferramentas experimentais. |
| [#3580](https://github.com/ventoy/Ventoy/pull/3580) — Update Korean | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3581](https://github.com/ventoy/Ventoy/pull/3581) — Update Korean | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3582](https://github.com/ventoy/Ventoy/pull/3582) — Update ko_KR.txt | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3583](https://github.com/ventoy/Ventoy/pull/3583) — Update Russian translation | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3601](https://github.com/ventoy/Ventoy/pull/3601) — Add support for custom persistence config files | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3604](https://github.com/ventoy/Ventoy/pull/3604) — Update sr_RS.txt | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3605](https://github.com/ventoy/Ventoy/pull/3605) — Update sr_RS.json | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3617](https://github.com/ventoy/Ventoy/pull/3617) — Add Windows CLI feature parity with Unix installer | Adaptado | CLI Windows ampliada; resolução preserva checks de pacote para escrita e libera comandos informativos. Código Windows não compilado/executado aqui. |
| [#3618](https://github.com/ventoy/Ventoy/pull/3618) — Fix MSVC warnings in vendored FatFs and xz-embedded | Integrado | Casts explícitos e máscara LBA_t incorporados. Build MSVC não disponível para validar avisos e importações. |
| [#3619](https://github.com/ventoy/Ventoy/pull/3619) — Trim DelayLoadDLLs to DLLs actually imported (fix LNK4199) | Integrado | Listas DelayLoadDLLs reduzidas às importações propostas. Verificação do linker MSVC permanece pendente. |
| [#3659](https://github.com/ventoy/Ventoy/pull/3659) — Bug Fix: missing bounds check in vtoy_json_escape_string | Adaptado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3691](https://github.com/ventoy/Ventoy/pull/3691) — Update pt-BR translation | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3692](https://github.com/ventoy/Ventoy/pull/3692) — fix: use bounded strlcpy/snprintf in grub-install-common.c... | Integrado | Diff real revisado: troca strcpy por memcpy em buffer já dimensionado e reorganiza liberação de locales; a descrição original superestima a vulnerabilidade e não corresponde integralmente ao patch. |
| [#3711](https://github.com/ventoy/Ventoy/pull/3711) — Added Santali translation & Fixed Hindi locale files | Integrado | Santali adicionado e Hindi renomeado para hi_IN. Parser Plugson atualizado para locales de seis caracteres como sat_IN, com regressão C e compatibilidade com listas antigas. |
| [#3721](https://github.com/ventoy/Ventoy/pull/3721) — fix(docs): correct typos found during code review | Adaptado | Correções de texto incorporadas sem sobrescrever os builds atuais; codificações de arquivos Windows preservadas. |
| [#3729](https://github.com/ventoy/Ventoy/pull/3729) — Update Traditional Chinese GRUB translations (AI-assisted) | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3747](https://github.com/ventoy/Ventoy/pull/3747) — Fix spelling and accentuation in pt_BR.json | Integrado | Tradução pt-BR incorporada com acentos recuperados e conciliação com as outras contribuições pt-BR. |
| [#3755](https://github.com/ventoy/Ventoy/pull/3755) — Build modernization and ISO test matrix | Adaptado | Build reproduzível e matriz QEMU incorporados como workflows manuais experimentais. Falhas de compilação propagadas, verificação exige artefatos reconstruídos, imagens virtuais usam payloads reais de releases e screenshot isolada não comprova boot. |
| [#3776](https://github.com/ventoy/Ventoy/pull/3776) — Update languages.json | Integrado | Tradução catalã incorporada; campo Author JSON reparado e créditos preservados. |
| [#3786](https://github.com/ventoy/Ventoy/pull/3786) — Update Azerbaijani language | Integrado | Tradução incorporada e conciliada por idioma/chave; estrutura JSON verificada. Não houve revisão linguística por falante nativo. |
| [#3788](https://github.com/ventoy/Ventoy/pull/3788) — Create a Ventoy bootable USB directly from the EFI environment. | Adaptado | Texto preservado em DOC/Proposals/EFI-tool.md como proposta sem implementação; README principal não foi substituído por alegações de funcionalidade inexistente. |
| [#3790](https://github.com/ventoy/Ventoy/pull/3790) — Korean language update | Integrado | Atualização coreana incorporada mantendo também o crédito anterior HYB1022. |
