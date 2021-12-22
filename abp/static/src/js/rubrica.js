/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";

const { useSubEnv, useContext } = owl.hooks;
const { xml } = owl.tags;
const { Context } = owl;

class Rubrica extends owl.Component {

    setup() {
        this.model = useModel(rubricaModel, {
            resModel: this.props.resModel,
            domain: this.props.domain,
        });
    }
}

Rubrica.type = "rubrica";
Rubrica.display_name = "Rubrica";
Rubrica.icon = "fa-check-square";
Rubrica.multiRecord = false;
Rubrica.searchMenuTypes = ["filter", "favorite","groupBy"];
Rubrica.components = { Layout };
Rubrica.template = "abp.rubrica_template";

registry.category("views").add("rubrica", Rubrica);



class rubricaModel extends Model {
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
  rubricaModel.services = ["orm"];
  // El servicio ORM es una abstracción sobre RPC para manejar las peticiones 
  // al servidor con una sintaxis similar al backend