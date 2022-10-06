# REST API anti-plagiarism

## <u>Разобранны следующие операции:</u>
- GET:       /                    - Main page.
- GET:       /file-upload         - Интерфейс для загрузки архива.
- POST:      /file-upload         - Загружает zip архив с программами и проверяет их на плагиат.

### <u>Для запуска приложения (Предварительно должны быть установлены docker и docker-compose):</u>
```
make build && make run
```

### Если требуется прекратить работу сервиса:
```
make app_down
```

### To send test zip archive to server:

- ```
    make test
    ```

- ```
    curl -X POST -F 'file=@programs/different_qsort_solutions.zip' http://127.0.0.1/file-upload
    ```
### Or send your own archive:
- using a request similar to the above
    ```
    curl -X POST -F 'file=@path/to/your/archive.zip' http://127.0.0.1/file-upload
    ```

- send through [graphic interface](http://127.0.0.1/).

![Upload files](.photos/1.png)
![Example of output](.photos/2.png)