/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";

import AbstractFieldOwl from "web.AbstractFieldOwl";
import fieldUtils from 'web.field_utils';
import field_registry from 'web.field_registry_owl';


const { useSubEnv, useContext } = owl.hooks;
const { xml } = owl.tags;
const { Context } = owl;


const { useState } = owl.hooks;

class Switch extends AbstractFieldOwl {

  setup(){
    //  console.log('setup',JSON.stringify(this.record.fields),this.dataPointId,this.value,this.name,this.formatType,this.field);
      this.state = useState({value: this.value ? JSON.parse(this.value) : null});
      // useState es un hook que crea un observable con el valor que recibe el widget
  }

  _onChange() {
    if (this.mode === 'edit') {
      console.log(this.state.value);
      this._setValue(this.state.value);
    }
    /* setValue retorna una promesa de enviar un trigger llamado field-changed 
    ese trigger lo recogerá el componente padre para cambiar el valor en el modelo
    Además, lo hace compatible con los widgets antiguos y los componentes modernos
     */
  }

}

Switch.template = 'abp.switch_template';
field_registry.add('abp_switch', Switch);



class RubricaNivel  extends owl.Component {
  setup(){
    console.log(this.props);
    this.nivel = this.props.nivel;   
    if (this.nivel.puntuacion) {
    this.record = {
      id: this.nivel.puntuacion.id, 
      data:  this.nivel.puntuacion, 
      fields:  {"logrado":{"id":null,"select":null,"views":{},"type":"boolean","change_default":false,"company_dependent":false,"depends":[],"manual":false,"readonly":false,"required":false,"searchable":true,"sortable":true,"store":true,"string":"Logrado","name":"logrado"}},
      fieldsInfo: {}
    }
  }

  }

 /* _onFieldChanged(event){
    console.log(event.detail.changes);
    this.trigger('field-changed',event.detail.changes)
  }*/



}

RubricaNivel.components = { Switch: field_registry.get('abp_switch') }
RubricaNivel.template = "abp.rubrica_nivel_template";


// Arch parser para arch (addons/web/static/src/views/pivot)



class Rubrica extends owl.Component {

    setup() {
      console.log(this.props);
        this.model = useModel(rubricaModel, {
            resModel: this.props.resModel,
            domain: this.props.domain,
        });
       // console.log(this.model);
    }

    _onFieldChanged(event){
     console.log('Changes: ',event.detail);
     
    }
  
  //  static components = { RubricaNivel }
}

Rubrica.type = "rubrica";
Rubrica.display_name = "Rubrica";
Rubrica.icon = "fa-check-square";
Rubrica.multiRecord = false;
Rubrica.searchMenuTypes = ["filter", "favorite","groupBy"];
Rubrica.components = { Layout, RubricaNivel };
Rubrica.template = "abp.rubrica_template";

registry.category("views").add("rubrica", Rubrica);



class rubricaModel extends Model {
    static services = ["orm"];
  
    setup(params, { orm }) {  // es necesario pasar un servicio al modelo, normalmente orm
      console.log(params);
      this.model = params.resModel;  //El modelo
      this.orm = orm; // El servicio ORM
      this.keepLast = new KeepLast(); // Una utilidad para manejar una lista de promesas
      // Y mantener la última activa
    }
  
    async load(params) {
      
      this.data = await this.keepLast.add(  // Descargar los datos principales de la rubrica
        this.orm.searchRead(this.model, params.domain, [], { limit: 100 })
      );

      const indicadores = await this.keepLast.add( // De la rúbrica descargar los indicadores 
        this.orm.read('abp.indicador', this.data[0].indicadores, [], {})
      ); // indicar bien el modelo por arch y el nombre del many2many en la rubrica
    // console.log(indicadores,indicadores.map(i=> i.niveles.length));

      const niveles = await this.keepLast.add( // De la rúbrica descargar los niveles 
        this.orm.read('abp.nivel', this.data[0].niveles, [], {})
      ); // indicar bien el modelo por arch y el nombre del many2many en la rubrica
     // this.data[0].niveles = niveles;

      const puntuaciones = await this.keepLast.add( // De la rúbrica descargar los puntuaciones 
        this.orm.read('abp.puntuacion', this.data[0].puntuaciones, [], {})
      ); // indicar bien el modelo por arch y el nombre del many2many en la rubrica
      //this.data[0].puntuaciones = puntuaciones;
      console.log( this.data[0].puntuaciones);

      const indicadoresNiveles = indicadores.map(i=>{
        let iniveles = niveles
          .filter(n=> n.indicador[0] === i.id)
          .map(n=> { 
            return {
              ...n,
              puntuacion: puntuaciones.filter(p => p.nivel[0] == n.id )[0],
             
            }; 
          })
          .sort((a,b)=> a.ponderacion - b.ponderacion )
        
        let indicador = {...i,niveles: iniveles}
        return indicador;
      })
      // colspan sirve para saver cuantos niveles como máximo tenemos y ajustar la tabla
      const colspan = Math.max(...indicadores.map(i=> i.niveles.length));
      this.colspan = colspan;

      this.data[0].indicadores = indicadoresNiveles;

      this.dataJSON = JSON.stringify(this.data);  // para probar los datos en la pantalla
      this.notify();  // Notifica a los subscriptores con useModel
    }


    async update(params){
      this.data = await this.keepLast.add( 
        this.orm.write(this.model, params.domain, [], { limit: 100 })
      );
    }
  }
  rubricaModel.services = ["orm"];
  // El servicio ORM es una abstracción sobre RPC para manejar las peticiones 
  // al servidor con una sintaxis similar al backend











  