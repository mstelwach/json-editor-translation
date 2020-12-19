# json-editor-translation

Prosta aplikacja internetowa do edycji plików JSON zawierających tłumaczenia

Załaduj translację i w łatwy sposób uzupełnij brakujące etykiety tłumaczeniami.

## Front-end

#### `npm-lite-server`

lite-server to lekki programistyczny serwer WWW z obsługą aplikacji jednostronicowych (SPA).
Nasza aplikacja wykorzystuje lite-server.

W głównym katalogu projektu możesz uruchomić aplikację, wykonując komendę:
  ```
  $ npm start
  ```

Aplikacja jest uruchmiana w trybie deweloperskim. <br />
Otwórz [http://localhost:3000](http://localhost:3000), aby wyświetlić w przeglądarce.

## Back-end

#### `python`
Jeżeli chcesz porównać tłumaczenia i uzupełnić brakujące etykiety w aplikacji frontendowej, wykorzystaj skrypt:
#### `json-editor.py`

Aby skryptu:
  1. Przejdź do katologu `./backend`
  2. Otwórz terminal, a następnie wprowadź następujące polecenia:
  
- Porównanie głównego tłumaczenia z pozostałymi translacjami pod względem nieprzetłumaczonych etykiet.
    Utworzenie pliku `.json` z brakującymi etykietami lub błędnie przetłumaczonymi (plik wykorzystujemy w aplikacji)
    
    Przykładowe dane wejściowe: 
    - `en_US.JSON` - nazwa pliku głównego tłumaczenia
    - `es.json` - nazwa pliku tłumaczenia z brakującymi etykietami
     ```
  $ python json-editor.py -set_untranslated_labels 'en_US.JSON' 'es.json'
     ```
    Przykładowe dane wyjściowe: Utworzenie pliku `en-US_es-ES.json` w katalogu `backend/translations/untranslated_labels`.
    
- Wprowadzenie przetłumaczonych etykiet danego języka do źródłowego pliku translacji
    
    Przykładowe dane wejściowe: 
    - `en-US_es-ES.json` - zaktualizowany plik z przetłumaczonymi etykietami
    - `es-ES` - język tłumaczeń, który chcemy zaktualizować
    - `es.json` - nazwa pliku tłumaczenia źródłowego do zaktualizowania
    
     ```
  $ python json-editor.py -update_translations 'en-US_es-ES.json' 'es-ES' 'es.json'
     ```

### Narzędzia do uruchomienia aplikacji i skryptu:
* [python] - https://www.python.org/
* [npm] - https://www.npmjs.com/

#### TO WSZYSTKO!