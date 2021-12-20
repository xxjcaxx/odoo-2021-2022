/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";
import AbstractFieldOwl from "web.AbstractFieldOwl";
import fieldUtils from 'web.field_utils';
import field_registry from 'web.field_registry_owl';

const { useState } = owl.hooks;


class Slider extends AbstractFieldOwl {

    setup(){
        console.log('setup');
        this.state = useState({value: this.value ? JSON.parse(this.value) : null});
        // useState es un hook que crea un observable con el valor que recibe el widget
    }

    _onChange() {
      if (this.mode === 'edit') {
        this._setValue(this.state.value);
      }
    }

}

Slider.template = 'provesowl.slider_template';

field_registry.add('provesowl-slider', Slider);

export default Slider;



