import json
import re
import sys


class CompareTranslations:

    def __init__(self):
        self.languages_translation = []
        self.untranslated_labels = {}

    def get_untranslated_labels(self):
        """
        :return: Funkcja zwraca słownik nieprzetłumaczonych etykiet w podanych językach.
        """
        return self.untranslated_labels

    def get_languages_translation(self):
        """
        :return: Funkcja zwraca listę tłumaczonych języków.
        """
        return self.languages_translation

    @staticmethod
    def get_dict_from_json_file(file, path_file):
        """
        Konwertowanie pliku '.json' na słownik.
        :param file: format 'string', nazwa pliku '.json', np: 'es.json'
        :param path_file: format 'string', ścieżka docelowa pliku, np: './translations/
        :return: Funkcja zwraca słownik {klucz : wartość}.
        """
        with open('{}/{}'.format(path_file, file)) as json_file:
            dict_items = json.load(json_file)
        return dict_items

    def set_untranslated_label(self, translations_dict, label, language, main_translation_dict):
        """
        Dodanie nieprzetłumaczonej etykiety danego języka do głównego słownika 'untranslated_labels'
        :param translations_dict: format 'dict'; słownik ze źródłowymi tłumaczeniami z danymi językami
        :param label: format 'string'; etykieta tłumaczenia, np: 'orientation_type_vertical'
        :param language: format 'string'; język tłumaczenia, np: 'es-ES'
        :param main_translation_dict: format 'dict'; słownik z największą ilością etykiet
        :return: Funkcja zwraca wartość 'True', jeżeli etykieta została dodana. W odwrotnym przypadku wartość 'False'
        """
        if label not in translations_dict[language] or \
                main_translation_dict[label] == translations_dict[language][label]:
            self.untranslated_labels[label][language] = ''
            return True
        return False

    def set_untranslated_labels(self, main_translation, *translations):
        """
        Porównanie wyżej wymienionych tłumaczeń (translations) z głównym tłumaczeniem pod względem nieprzetłumaczonych
        etykiet.
        Funkcja tworzy plik '.json' z brakującymi etykietami lub błędnie przetłumaczonymi,
        np: {Nazwa etykiety: {en-US: tłumaczenie, es-ES: ''}}
        :param main_translation: format 'string'; nazwa pliku głównego tłumaczenia, np: 'en_US.JSON
        :param translations: format 'string'; nazwy plików z tłumaczeniami,
        np: 'es.json' lug "'es.json', 'de-DE.json'"
        :return: Funkcja zwraca informację o utworzeniu pliku i ilość nieprzetłumaczonych etykiet.
        """
        translations_dict = {}
        main_translation_dict = self.get_dict_from_json_file(main_translation, './translations')
        translations = [main_translation] + list(translations)
        for translation in translations:
            language = re.sub(r'\.[a-zA-Z]+', '', translation).replace('_', '-')
            if '-' not in language:
                language += '-{}'.format(language.upper())
            self.languages_translation.append(language)
            translations_dict[language] = self.get_dict_from_json_file(translation, './translations')

        max_labels_language = max(translations_dict, key=lambda lang: len(translations_dict[lang]))
        if len(translations_dict[max_labels_language]) > len(main_translation_dict):
            return 'Główne tłumaczenie jest błędne! Liczba etykiet jest za mała.'
        del translations_dict[max_labels_language]

        for label in main_translation_dict:
            self.untranslated_labels[label] = {max_labels_language: main_translation_dict[label]}
            untranslated_label = False
            for language in translations_dict:
                untranslated_label = self.set_untranslated_label(translations_dict,
                                                                 label,
                                                                 language,
                                                                 main_translation_dict)

            if not untranslated_label:
                del self.untranslated_labels[label]

        self.set_json_file_from_dict(self.untranslated_labels, './translations/untranslated_labels')
        return 'Plik został zapisany! Liczba nieprzetłumaczonych etykiet: {}'.format(len(self.untranslated_labels))

    def set_json_file_from_dict(self, translation_dict, path_file):
        """
        Konwertowanie słownika na plik '.json' oraz zapisanie na dysku lokalnym.
        :param translation_dict: format 'dict'; słownik nieprzetłumaczonych etykiet lub słownik tłumaczenia źródłowego
        do zaktualizowania
        :return:
        """
        file_name = '{}.json'.format('_'.join(self.languages_translation))
        with open('{}/{}'.format(path_file, file_name), 'w') as json_file:
            json.dump(translation_dict, json_file, indent=2, ensure_ascii=False)

    def update_translations(self, untranslated_label_file, language, translation_file):
        """
        Dodanie do istniejącego pliku prawidłowych tłumaczeń.
        :param untranslated_label_file: format 'string'; zaktualizowany plik z przetłumaczonymi etykietami,
        np: 'en-US_es-ES.json
        :param language: format 'string'; język tłumaczeń, który chcemy zaktualizować, np: 'es-ES'
        :param translation_file: format 'string'; nazwa pliku tłumaczenia źródłowego do zaktualizowania, np: 'es.json'
        :return: Funkcja zwraca informacje o prawidłowym zaktualizowaniu i liczbę dodanych przetłumaczonych etykiet.
        """
        if language not in untranslated_label_file:
            return "Nieprawidłowy język! Brak języka '{}' w źródłowym tłumaczeniu".format(language)

        labels = self.get_dict_from_json_file(untranslated_label_file, './translations/untranslated_labels/')
        translation = self.get_dict_from_json_file(translation_file, './translations')

        counter_translated_labels = 0
        for label in labels:
            if labels[label].get(language, None):
                translation[label] = labels[label][language]
                counter_translated_labels += 1

        with open('translations/{}'.format(translation_file), 'w') as json_file:
            json.dump(translation, json_file, indent=2, ensure_ascii=False)
        return 'Tłumaczenie zaktualizowane! Liczba dodanych etykiet: {}'.format(counter_translated_labels)


if __name__ == '__main__':
    c = CompareTranslations()
    method = sys.argv[1].lstrip('-')
    args = sys.argv[2:]
    print(getattr(c, method)(*args))
