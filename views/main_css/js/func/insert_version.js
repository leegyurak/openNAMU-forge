"use strict";

function opennamu_forge_do_insert_version(dom_name_version_now, dom_name_version_new) {
    fetch("/api/version").then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return response.json();
    }).then(get_data => {
        document.getElementById(dom_name_version_now).innerHTML += get_data['version'];

        const repository = window.OPENNAMU_FORGE_UPDATE_REPOSITORY || 'opennamu-forge/opennamu-forge';
        return fetch(`https://raw.githubusercontent.com/${repository}/${get_data['build']}/version.json`);
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }).then(versionData => {
        if(versionData['beta'] !== undefined) {
            document.getElementById(dom_name_version_new).innerHTML += versionData['beta']['r_ver'];
        } else {
            document.getElementById(dom_name_version_new).innerHTML += versionData['r_ver'];
        }
    }).catch(error => {
        console.error('Error:', error);
    });
    
}

let opennamu_forge_do_insert_version_url = [
    '/manager/1',
    '/manager',
    '/update'
];
if(opennamu_forge_do_insert_version_url.includes(window.location.pathname)) {
    opennamu_forge_do_insert_version('ver_send_2', 'ver_send');
}
