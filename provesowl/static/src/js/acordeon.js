/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";

const { useSubEnv, useContext } = owl.hooks;
const { xml } = owl.tags;
const { Context } = owl;

class AcordeonBanner extends owl.Component {
    static template = xml`
    <div>
      <h1>Abiertos: <t t-esc="abiertos.abiertos"/></h1>
    </div>`;

    abiertos = useContext(this.env.abiertosContext);  // Hook para escuchar el context

}

class Acordeon extends owl.Component {
    setup() { // Definimos el modelo que nutrirá de datos
      this.model = useModel(BasicModel, {  // useModel: Hook para subscribirse al modelo
        resModel: this.props.resModel,  // Obtenemos datos del componente paddre
        domain: this.props.domain,  // por propagación con "props"
      });

      // Para el banner
      let config = this.env.config;
      let searchModel = this.env.searchModel;
      console.log(config,searchModel);


      const abiertosContext = new Context({ abiertos: 0 });
      this.env.abiertosContext = abiertosContext;  // crear un nuevo context con los acordeones abiertos

      config.Banner = AcordeonBanner;      
      searchModel.display = {
        controlPanel: true,
        banner: true,
      };
      useSubEnv({
        searchModel: searchModel,
        config: { ...config },
      });
  

      
  
    }
  }

  Acordeon.type = "acordeon"; 
  Acordeon.display_name = "Acordeon";
  Acordeon.icon = "fa-align-justify";  // Un icono parecido al acordeón
  Acordeon.multiRecord = true;
  Acordeon.searchMenuTypes = ["filter", "favorite","groupBy"];
  Acordeon.components = { Layout };   // Layout: Componente que ayuda a hacer la vista
  // Añade el searchPanel, el ControlPanel y el Banner. Se usa como Wrapper de la plantilla
  Acordeon.template = "provesowl.acordeon_template";
  
  registry.category("views").add("acordeon", Acordeon);
  // Registramos la vista en el frontend

class BasicModel extends Model {
    static services = ["orm"];
  
    setup(params, { orm }) {  // es necesario pasar un servicio al modelo, normalmente orm
      this.model = params.resModel;  //El modelo
      this.orm = orm; // El servicio ORM
      this.keepLast = new KeepLast(); // Una utilidad para manejar una lista de promesas
      // Y mantener la última activa
    }
  
    async load(params) {
      this.data = await this.keepLast.add(
        this.orm.searchRead(this.model, params.domain, [], { limit: 100 })
      );
      this.notify();  // Notifica a los subscriptores con useModel
    }
  }
  BasicModel.services = ["orm"];
  // El servicio ORM es una abstracción sobre RPC para manejar las peticiones 
  // al servidor con una sintaxis similar al backend

  
 