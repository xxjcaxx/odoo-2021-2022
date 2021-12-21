/** @odoo-module **/

const { useState } = owl.hooks;  // Object destructuring per treue el que necessitem
const { xml } = owl.tags;  //xml helper per parsejar xml
const { Component } = owl;  // Com es veu, owl està disponible en l'espai de noms del bundle per a que es puga accedir fàcilment.

class MyComponent extends Component {
    setup() {  // Al no poder sobreescriure constructor, el que Odoo ens dona és 
        // la funció setup() que sí la poden modificar
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value++;
    }
}

// La forma de cridar a la funció xml en tagged templates 
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#tagged_templates

MyComponent.template = xml`<button t-on-click="changeText">  
Click Me! [<t t-esc="state.value"/>]
</button>`;

// Aquesta manera no és la millor, és millor definir els xml en un fitxer a banda.
