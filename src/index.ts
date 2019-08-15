// Copyright (c) LSST DM/SQuaRE
// Distributed under the terms of the MIT License.

import {
  Menu
} from '@phosphor/widgets';

import {
  showDialog, Dialog
} from '@jupyterlab/apputils';

import {
  IMainMenu
} from '@jupyterlab/mainmenu';

import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  IDocumentManager
} from '@jupyterlab/docmanager';


import {
  ServiceManager, ServerConnection
} from '@jupyterlab/services';

import {
  PageConfig
} from '@jupyterlab/coreutils';

import {
  Widget
} from '@phosphor/widgets';

/**
 * The command IDs used by the plugin.
 */
export
namespace CommandIDs {
  export const lsstquery: string = 'lsstquery';
};

/**
 * Interface used by the extension
 */
interface PathContainer {
  path: string;
}


/**
 * Activate the extension.
 */
function activateLSSTLabExtensions(app: JupyterFrontEnd, mainMenu: IMainMenu, docManager: IDocumentManager): void {

  console.log('jupyterlab-lsstextensions: activated')

  let svcManager = app.serviceManager;

  app.commands.addCommand(CommandIDs.lsstquery, {
    label: 'Open from Query ID...',
    caption: 'Open notebook from supplied query ID',
    execute: () => {
      lsstQuery(app, docManager, svcManager)
    }
  });

  // Add commands and menu itmes.
  const menu = new Menu({ commands: app.commands })
  menu.addItem({ command: CommandIDs.lsstquery })
  menu.title.label = "LSST"
  mainMenu.addMenu(menu, {
    rank: 420,
  });
}

class QueryHandler extends Widget {
  constructor() {
    super({ node: Private.createQueryNode() });
    this.addClass('lsst-qh')
  }

  get inputNode(): HTMLInputElement {
    return this.node.getElementsByTagName('input')[0] as HTMLInputElement;
  }

  getValue(): string {
    return this.inputNode.value;
  }
}



function queryDialog(manager: IDocumentManager): Promise<string | null> {
  let options = {
    title: 'Query ID',
    body: new QueryHandler(),
    focusNodeSelector: 'input',
    buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'CREATE' })]
  }
  return showDialog(options).then(result => {
    console.log("Result from queryDialog: ", result)
    if (!result.value) {
      console.log("No result.value from queryDialog");
      return null;
    }
    if (result.button.label === 'CREATE') {
      console.log("Got result ", result.value, " from queryDialog: CREATE")
      return Promise.resolve(result.value);
    }
    console.log("Did not get queryDialog: CREATE")
    return null;
  });
}

function apiRequest(url: string, init: RequestInit, settings: ServerConnection.ISettings): Promise<PathContainer> {
  /**
  * Make a request to our endpoint to get a pointer to a templated
  *  notebook for a given query
  *
  * @param url - the path for the query extension
  *
  * @param init - The POST + body for the extension
  *
  * @param settings - the settings for the current notebook server.
  *
  * @returns a Promise resolved with the JSON response
  */
  // Fake out URL check in makeRequest
  let newSettings = ServerConnection.makeSettings({
    baseUrl: settings.baseUrl,
    appUrl: settings.appUrl,
    wsUrl: settings.wsUrl,
    init: settings.init,
    token: settings.token,
    Request: settings.Request,
    Headers: settings.Headers,
    WebSocket: settings.WebSocket
  });
  return ServerConnection.makeRequest(url, init, newSettings).then(
    response => {
      if (response.status !== 200) {
        return response.json().then(data => {
          throw new ServerConnection.ResponseError(response, data.message);
        });
      }
      return response.json();
    });
}

function lsstQuery(app: JupyterFrontEnd, docManager: IDocumentManager, svcManager: ServiceManager): void {
  queryDialog(docManager).then(queryid => {
    console.log("queryid is", queryid)
    if (!queryid) {
      console.log("queryid was null")
      return new Promise((res, rej) => { })
    }
    // Figure out some more generic way to get params
    let body = JSON.stringify({ "query_id": queryid })
    let endpoint = PageConfig.getBaseUrl() + "lsstquery"
    let init = {
      method: "POST",
      body: body
    }
    let settings = svcManager.serverSettings
    apiRequest(endpoint, init, settings).then(function(res) {
      let path = res.path
      docManager.open(path)
    });
    return new Promise((res, rej) => { })
  });
}


/**
 * Initialization data for the jupyterlab-lsstquery extension.
 */
const LSSTLabExtensions: JupyterFrontEndPlugin<void> = {
  activate: activateLSSTLabExtensions,
  id: 'jupyter.extensions.jupyterlab-lsst-extension',
  requires: [
    IMainMenu,
    IDocumentManager
  ],
  autoStart: true,
};

export default LSSTLabExtensions

namespace Private {
  /**
   * Create node for query handler.
   */

  export
    function createQueryNode(): HTMLElement {
    let body = document.createElement('div');
    let qidLabel = document.createElement('label');
    qidLabel.textContent = 'Enter Query ID';
    let name = document.createElement('input');
    body.appendChild(qidLabel);
    body.appendChild(name);
    return body;
  }
}
