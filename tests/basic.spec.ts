/**
 * Copyright (c) Microsoft Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { test, expect } from './fixtures';

test('test tool list', async ({ server }) => {
  const list = await server.send({
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/list',
  });

  expect(list).toEqual(expect.objectContaining({
    id: 1,
    result: expect.objectContaining({
      tools: [
        expect.objectContaining({
          name: 'browser_navigate',
        }),
        expect.objectContaining({
          name: 'browser_go_back',
        }),
        expect.objectContaining({
          name: 'browser_go_forward',
        }),
        expect.objectContaining({
          name: 'browser_snapshot',
        }),
        expect.objectContaining({
          name: 'browser_click',
        }),
        expect.objectContaining({
          name: 'browser_hover',
        }),
        expect.objectContaining({
          name: 'browser_type',
        }),
        expect.objectContaining({
          name: 'browser_select_option',
        }),
        expect.objectContaining({
          name: 'browser_press_key',
        }),
        expect.objectContaining({
          name: 'browser_wait',
        }),
        expect.objectContaining({
          name: 'browser_save_as_pdf',
        }),
        expect.objectContaining({
          name: 'browser_close',
        }),
      ],
    }),
  }));
});

test('test resources list', async ({ server }) => {
  const list = await server.send({
    jsonrpc: '2.0',
    id: 2,
    method: 'resources/list',
  });

  expect(list).toEqual(expect.objectContaining({
    id: 2,
    result: expect.objectContaining({
      resources: [
        expect.objectContaining({
          uri: 'browser://console',
          mimeType: 'text/plain',
        }),
      ],
    }),
  }));
});

test('test browser_navigate', async ({ server }) => {
  const response = await server.send({
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'browser_navigate',
      arguments: {
        url: 'data:text/html,<html><title>Title</title><body>Hello, world!</body></html>',
      },
    },
  });

  expect(response).toEqual(expect.objectContaining({
    id: 2,
    result: {
      content: [{
        type: 'text',
        text: `
- Page URL: data:text/html,<html><title>Title</title><body>Hello, world!</body></html>
- Page Title: Title
- Page Snapshot
\`\`\`yaml
- document [ref=s1e2]: Hello, world!
\`\`\`
`,
      }],
    },
  }));
});

test('test browser_click', async ({ server }) => {
  await server.send({
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'browser_navigate',
      arguments: {
        url: 'data:text/html,<html><title>Title</title><button>Submit</button></html>',
      },
    },
  });

  const response = await server.send({
    jsonrpc: '2.0',
    id: 3,
    method: 'tools/call',
    params: {
      name: 'browser_click',
      arguments: {
        element: 'Submit button',
        ref: 's1e4',
      },
    },
  });

  expect(response).toEqual(expect.objectContaining({
    id: 3,
    result: {
      content: [{
        type: 'text',
        text: `\"Submit button\" clicked

- Page URL: data:text/html,<html><title>Title</title><button>Submit</button></html>
- Page Title: Title
- Page Snapshot
\`\`\`yaml
- document [ref=s2e2]:
  - button \"Submit\" [ref=s2e4]
\`\`\`
`,
      }],
    },
  }));
});

test('test reopen browser', async ({ server }) => {
  const response2 = await server.send({
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'browser_navigate',
      arguments: {
        url: 'data:text/html,<html><title>Title</title><body>Hello, world!</body></html>',
      },
    },
  });

  expect(response2).toEqual(expect.objectContaining({
    id: 2,
  }));

  const response3 = await server.send({
    jsonrpc: '2.0',
    id: 3,
    method: 'tools/call',
    params: {
      name: 'browser_close',
    },
  });

  expect(response3).toEqual(expect.objectContaining({
    id: 3,
    result: {
      content: [{
        text: 'Page closed',
        type: 'text',
      }],
    },
  }));

  const response4 = await server.send({
    jsonrpc: '2.0',
    id: 4,
    method: 'tools/call',
    params: {
      name: 'browser_navigate',
      arguments: {
        url: 'data:text/html,<html><title>Title</title><body>Hello, world!</body></html>',
      },
    },
  });

  expect(response4).toEqual(expect.objectContaining({
    id: 4,
    result: {
      content: [{
        type: 'text',
        text: `
- Page URL: data:text/html,<html><title>Title</title><body>Hello, world!</body></html>
- Page Title: Title
- Page Snapshot
\`\`\`yaml
- document [ref=s1e2]: Hello, world!
\`\`\`
`,
      }],
    },
  }));
});

test.describe('test browser_select_option', () => {
  test('single option', async ({ server }) => {
    await server.send({
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/call',
      params: {
        name: 'browser_navigate',
        arguments: {
          url: 'data:text/html,<html><title>Title</title><select><option value="foo">Foo</option><option value="bar">Bar</option></select></html>',
        },
      },
    });

    const response = await server.send({
      jsonrpc: '2.0',
      id: 3,
      method: 'tools/call',
      params: {
        name: 'browser_select_option',
        arguments: {
          element: 'Select',
          ref: 's1e4',
          values: ['bar'],
        },
      },
    });

    expect(response).toEqual(expect.objectContaining({
      id: 3,
      result: {
        content: [{
          type: 'text',
          text: `Selected option in \"Select\"

- Page URL: data:text/html,<html><title>Title</title><select><option value="foo">Foo</option><option value="bar">Bar</option></select></html>
- Page Title: Title
- Page Snapshot
\`\`\`yaml
- document [ref=s2e2]:
  - combobox [ref=s2e4]:
    - option \"Foo\" [ref=s2e5]
    - option \"Bar\" [selected] [ref=s2e6]
\`\`\`
`,
        }],
      },
    }));
  });

  test('multiple option', async ({ server }) => {
    await server.send({
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/call',
      params: {
        name: 'browser_navigate',
        arguments: {
          url: 'data:text/html,<html><title>Title</title><select multiple><option value="foo">Foo</option><option value="bar">Bar</option><option value="baz">Baz</option></select></html>',
        },
      },
    });

    const response = await server.send({
      jsonrpc: '2.0',
      id: 3,
      method: 'tools/call',
      params: {
        name: 'browser_select_option',
        arguments: {
          element: 'Select',
          ref: 's1e4',
          values: ['bar', 'baz'],
        },
      },
    });

    expect(response).toEqual(expect.objectContaining({
      id: 3,
      result: {
        content: [{
          type: 'text',
          text: `Selected option in \"Select\"

- Page URL: data:text/html,<html><title>Title</title><select multiple><option value="foo">Foo</option><option value="bar">Bar</option><option value="baz">Baz</option></select></html>
- Page Title: Title
- Page Snapshot
\`\`\`yaml
- document [ref=s2e2]:
  - listbox [ref=s2e4]:
    - option \"Foo\" [ref=s2e5]
    - option \"Bar\" [selected] [ref=s2e6]
    - option \"Baz\" [selected] [ref=s2e7]
\`\`\`
`,
        }],
      },
    }));
  });
});

test('browser://console', async ({ server }) => {
  await server.send({
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'browser_navigate',
      arguments: {
        url: 'data:text/html,<html><script>console.log("Hello, world!");console.error("Error"); </script></html>',
      },
    },
  });

  const response = await server.send({
    jsonrpc: '2.0',
    id: 3,
    method: 'resources/read',
    params: {
      uri: 'browser://console',
    },
  });
  expect(response).toEqual(expect.objectContaining({
    result: expect.objectContaining({
      contents: [{
        uri: 'browser://console',
        mimeType: 'text/plain',
        text: '[LOG] Hello, world!\n[ERROR] Error',
      }],
    }),
  }));
});

test('test batch processing in screenshot mode', async ({ server }) => {
  const fs = require('fs');
  const path = require('path');
  
  const testData = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/screenshot_test.json'), 'utf8'));
  
  const response = await server.send({
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/call',
    params: {
      name: 'batch_process',
      arguments: {
        input: testData
      }
    }
  });

  expect(response).toEqual(expect.objectContaining({
    id: 1,
    result: expect.objectContaining({
      content: [{
        type: 'text',
        text: expect.stringContaining('Successfully executed')
      }]
    })
  }));
});

test('test batch processing in snapshot mode', async ({ server }) => {
  const fs = require('fs');
  const path = require('path');
  
  const testData = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/snapshot_test.json'), 'utf8'));
  
  const response = await server.send({
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/call',
    params: {
      name: 'batch_process',
      arguments: {
        input: testData
      }
    }
  });

  expect(response).toEqual(expect.objectContaining({
    id: 1,
    result: expect.objectContaining({
      content: [{
        type: 'text',
        text: expect.stringContaining('Successfully executed')
      }]
    })
  }));
});
