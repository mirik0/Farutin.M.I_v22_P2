# Сравнение с apk dot

Для требования этапа 5 использованы три разных пакета из Alpine v3.22 main x86_64.
Данные и настоящий вывод apk-tools 2.14.9 сохранены 22.10.2026.
Код приложения читает APKINDEX самостоятельно; APK использовался для сравнения.

| Пакет | Версия | Связи нашего графа и apk dot |
| --- | --- | --- |
| busybox | 1.37.0-r20 | busybox -> musl |
| zlib | 1.3.2-r1 | zlib -> musl |
| xz | 5.8.4-r0 | xz -> musl, xz -> xz-libs, xz-libs -> musl |

Для всех трех пакетов наборы направленных связей совпадают.
Версия musl — 1.2.5-r13, xz-libs — 5.8.4-r0.

В `examples/` лежат три `.puml` нашего приложения и три `.apk.dot` штатного APK.
В `fixtures/alpine-sample.APKINDEX` сохранены необходимые записи индекса.

Штатные команды запускались с тем же локальным индексом:

```sh
mkdir -p /tmp/apk-root
apk --root /tmp/apk-root --arch x86_64 --allow-untrusted \
  --repository /repo --no-network add --initdb
apk --root /tmp/apk-root --arch x86_64 --allow-untrusted \
  --repository /repo --no-network dot busybox
apk --root /tmp/apk-root --arch x86_64 --allow-untrusted \
  --repository /repo --no-network dot zlib
apk --root /tmp/apk-root --arch x86_64 --allow-untrusted \
  --repository /repo --no-network dot xz
```

Локальный архив находился в `/repo/x86_64/APKINDEX.tar.gz`.
Пустой временный корень исключал влияние установленных пакетов.

Наш вывод использует PlantUML и имена пакетов, а штатный — Graphviz DOT,
версии в именах вершин и подписи библиотечных требований на связях.
Различия оформления не означают различий в зависимостях.
Поэтому сравниваются пары имен пакетов, а не строки файлов целиком.

Повторить сравнение на сохраненных данных:

```sh
python3 -m unittest discover -s tests -p test_examples.py -v
```

На других данных возможны различия: учебный код не решает совместную установку
с ограничениями версий и альтернативными поставщиками. Для зависимости без
точной версии берется первая запись индекса, для библиотеки — первый поставщик.
Точная версия корневого пакета учитывается всегда.
