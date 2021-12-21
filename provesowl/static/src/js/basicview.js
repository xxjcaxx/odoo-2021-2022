/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";

class BasicView extends owl.Component {
    setup() { // Definimos el modelo que nutrirá de datos
      this.model = useModel(BasicModel, {  // useModel: Hook para subscribirse al modelo
        resModel: this.props.resModel,  // Obtenemos datos del componente paddre
        domain: this.props.domain,  // por propagación con "props"
      });
    }
  }
  BasicView.type = "basic_view"; 
  BasicView.display_name = "BasicView";
  BasicView.icon = "fa-heart";
  BasicView.multiRecord = true;
  BasicView.searchMenuTypes = ["filter", "favorite"];
  BasicView.components = { Layout };   // Layout: Componente que ayuda a hacer la vista
  // Añade el searchPanel, el ControlPanel y el Banner. Se usa como Wrapper de la plantilla
  BasicView.template = owl.tags.xml/* xml */ `
  <Layout viewType="'basic_view'">
      <div><h1>Hello World</h1></div>
      <div t-foreach="model.data" t-as="record" t-key="record.id">
          <t t-esc="record.name"/>
      </div>
  </Layout>`;
  
  registry.category("views").add("basic_view", BasicView);
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

  
 