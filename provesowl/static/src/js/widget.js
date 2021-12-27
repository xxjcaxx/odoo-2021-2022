/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";
import AbstractFieldOwl from "web.AbstractFieldOwl";
import fieldUtils from 'web.field_utils';
import field_registry from 'web.field_registry_owl';
import { useService } from "@web/core/utils/hooks";

const { useState} = owl.hooks;
import { SERVICES_METADATA } from "@web/env";


//console.log(registry.category("services").get("contador"));

class Slider extends AbstractFieldOwl {
  
    setup(){
      const rpc = useService("rpc");
    /*  console.log("ENV:",this.env,
      "Service contador: ",registry.category("services").get("contador"),
      "RPC: ", registry.category("services").get("rpc"),
      SERVICES_METADATA, rpc
      );*/
      this.env.services.contador = registry.category("services").get("contador").start();
      this.compartido = useService("contador");
      this.state = useState({value: this.value ? JSON.parse(this.value) : null});
        // useState es un hook que crea un observable con el valor que recibe el widget
    }

    mounted(){
      this.compartido.bus.on("UPDATE",this,()=>{
        console.log('getvalue',this.compartido.getValue());
        this.state.value = this.compartido.getValue();
        this._setValue(this.state.value);
        this.render();
      });
    }

    willUnmount(){
      this.compartido.bus.off("UPDATE",this);
    }

    _onChange() {
      if (this.mode === 'edit') {
        this.compartido.change(this.state.value);
        this._setValue(this.state.value);
      }
    }

}

Slider.template = 'provesowl.slider_template';

field_registry.add('provesowl-slider', Slider);

export default Slider;



