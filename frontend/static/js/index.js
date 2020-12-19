let documentList;
let documentListItemTemplate;
let documentListTranslationLabelTemplate;
let counterUntranslatedLabel;
let fileName;

window.addEventListener('load', function() {
    documentList = document.getElementById('list');
    documentListItemTemplate = documentList.firstElementChild.cloneNode(true);
    documentListTranslationLabelTemplate = documentListItemTemplate.lastElementChild.cloneNode(true);
    getCachedData();
})

function loadJSONFile() {
    const fileInput = document.getElementById('file-import-input');
    if (fileInput.files.length) {
        let reader = new FileReader();
        reader.onload = (e) => {
            const jsonData = JSON.parse(e.target.result);
            JSONDataToHTML(jsonData)
        }
        reader.readAsText(fileInput.files[0])
    }
}
function setTranslationLabel(jsonData, label, labelType, language) {
    const newTranslationLabel = documentListTranslationLabelTemplate.cloneNode(true);
    let spanElementLanguage = newTranslationLabel.getElementsByTagName('span')[0];
    let inputElementLanguage = newTranslationLabel.getElementsByTagName('input')[0];
    if (labelType === 'object') {
        spanElementLanguage.innerText = language;
        // inputElementLanguage.setAttribute('id', `${language}-${label}`)
        inputElementLanguage.value = jsonData[label][language];
    } else if (labelType === 'string') {
        spanElementLanguage.innerText = 'Translation';
        inputElementLanguage.value = jsonData[label]
    }

    if (inputElementLanguage.value) {
        inputElementLanguage.classList.add('border', 'border-success')
    } else {
        inputElementLanguage.classList.add('border', 'border-danger')
    }
    return newTranslationLabel
}

function JSONDataToHTML(jsonData) {
    while (documentList.firstChild) {
        documentList.removeChild(documentList.lastChild);
    }
    for (let label in jsonData) {
        const newDocumentListItemTemplate = documentListItemTemplate.cloneNode(true);
        newDocumentListItemTemplate.removeChild(newDocumentListItemTemplate.lastElementChild);
        let labelHeader = newDocumentListItemTemplate.getElementsByClassName('label-header')[0];
        if (jsonData.hasOwnProperty(label)) {
            labelHeader.setAttribute('id', `${label}`);
            labelHeader.innerText = `${label}`;
            if (typeof jsonData[label] === 'object') {
                for (let language in jsonData[label]) {
                    if (jsonData[label].hasOwnProperty(language)) {
                        const newTranslationLabel = setTranslationLabel(jsonData, label, 'object', language);
                        newDocumentListItemTemplate.appendChild(newTranslationLabel)
                    }
                }
            } else if (typeof jsonData[label] === 'string') {
                const newTranslationLabel = setTranslationLabel(jsonData, label, 'string');
                newDocumentListItemTemplate.appendChild(newTranslationLabel)
            } else {
                break
            }
        }
        documentList.appendChild(newDocumentListItemTemplate)
    }
    documentList.style.display = 'block';
    setCounterUntranslatedLabel();
}

function textHTMLToJSONData() {
    const documentList = document.getElementById('list');
    let jsonData = {};
    let languageTranslation;
    let textTranslation;
    for (let i = 0; i < documentList.childElementCount; i++) {
        const label = documentList.children[i].getElementsByTagName('h5')[0].innerText;
        const translationLabels = documentList.children[i].getElementsByClassName('translation-label');
        console.log(translationLabels)
        if (translationLabels.length === 1) {
            textTranslation = translationLabels[0].getElementsByTagName('input')[0].value;
            jsonData[label] = textTranslation
        } else if (translationLabels.length > 1) {
            jsonData[label] = {};
            for (let j = 0; j < translationLabels.length; j++) {
                languageTranslation = translationLabels[j].getElementsByTagName('span')[0].innerText;
                textTranslation = translationLabels[j].getElementsByTagName('input')[0].value;
                jsonData[label][languageTranslation] = textTranslation
            }
        }
    }
    return jsonData
}

function jsonDataToJSONStringData(jsonData) {
    return JSON.stringify(jsonData, null, 2)
}

function exportJSONFile() {
    let exportFileName = document.getElementById('file-export-input').value + '.json';
    const jsonData = textHTMLToJSONData();
    const jsonStringData = jsonDataToJSONStringData(jsonData)
    downloadFile(jsonStringData, exportFileName)
}

function downloadFile(jsonStringData, fileName) {
    const fileSave = new Blob([jsonStringData], { type: "text/plain;charset=utf-8" });
    let a = document.createElement("a");
    a.download = fileName;
    a.href = URL.createObjectURL(fileSave)
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function getCachedData() {
    let data;
    if (Storage) {
        data = localStorage.getItem('translationData');
    }
    if (data) {
        const jsonData = JSON.parse(data);
        JSONDataToHTML(jsonData);
        console.log('Wczytano zachowane dane!')
    }

}

function setCachedData() {
    if (Storage) {
        const jsonData = textHTMLToJSONData();
        const jsonStringData = jsonDataToJSONStringData(jsonData);
        localStorage.setItem('translationData', jsonStringData);
        console.log('Dane zostały zapisane!')
    }
}

function setFileNameInput(input) {
    // let fileName;
    fileName = input.files[0].name.replace('.json', '');
    document.querySelector('.custom-file-label').innerHTML = fileName
    document.getElementById('file-export-input').value = fileName;
}

function validationInputTranslation(input) {
    if (input.value) {
        input.classList.remove('border-danger');
        input.classList.add('border-success');
    } else {
        input.classList.remove('border-success');
        input.classList.add('border-danger');
    }
    setCounterUntranslatedLabel()
}

function setCounterUntranslatedLabel() {
    let labels = documentList.querySelectorAll('.input-translation');
    let counter = 0;
    for (let i = 0; i < labels.length; i++) {
        if (!labels[i].value) {
            counter++
        }
    }
    document.querySelector('.counter-labels').innerHTML = `Untranslated Labels: <strong>${counter}</strong>`
}
