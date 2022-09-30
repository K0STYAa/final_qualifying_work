# REST API anti-plagiarism

## Разобранны следующие операции:
- POST:      /file-upload            - Загружает zip архив с программами и проверяет их на плагиат.

### Для запуска приложения (Предварительно должны быть установлены docker и docker-compose):
```
make build && make run
```

### Если требуется прекратить работу сервиса:
```
make db_down
```

### To send test zip archive to server:
```
make test
```
or
```
curl -X POST -F 'file=@programs/different_qsort_solutions.zip' http://127.0.0.1:80/file-upload
```