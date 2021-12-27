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

export const servicioEstadoCompartido = {
    dependencies: [],
    
    start( ){
      let value = 0;
      let bus = new owl.core.EventBus();
      return {
        change(newValue=1){
          value = newValue;
          console.log('change',value);
          bus.trigger("UPDATE");
        },
        getValue(){
          return value;
        },
        bus,
      };
    }
  };
  
  registry.category("services").add("contador",servicioEstadoCompartido);



const myService = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            notification.add(`Tick Tock ${counter++}`);
        }, 5000);
    }
};

//registry.category("services").add("myService", myService);
