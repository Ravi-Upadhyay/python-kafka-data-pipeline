import { html, css, LitElement } from 'lit';
import { io } from 'socket.io-client';

export class MeetupRsvpFe extends LitElement {
  static styles = css`
    :host {
      display: block;
      padding: 25px;
      color: var(--meetup-rsvp-fe-text-color, #000);
    }
  `;

  static properties = {
    header: { type: String },
    counter: { type: Number },
    socket: { type: Object },
    outputStack: { type: Array },
    kafkaOffset: { type: Number },
  };

  constructor() {
    super();
    this.header = 'Hey there';
    this.counter = 5;
    this.outputStack = [];
    this.kafkaOffset = 0;

    this.socket = io('http://localhost:5000');

    this.socket.on('connect', arg => {
      const logMessage = `WS:(Client), Socket id: ${this.socket.id}`;
      this.__outputLogger([logMessage, arg]);
    });

    this.socket.on('json', arg => {
      const logMessage = `WS:(Server), RSVP Data: ${JSON.stringify(arg)}`;
      this.__outputLogger([logMessage]);
    });

    this.socket.on('test', arg => {
      const logMessage = arg;
      this.__outputLogger([logMessage]);
    });
  }

  __outputLogger(messages, con = true) {
    // eslint-disable-next-line prefer-const
    for (let m of messages) {
      // eslint-disable-next-line no-console
      if (con === true) console.info(m);
      this.outputStack.push(m);
    }
    this.requestUpdate();
  }

  __cleanOutput() {
    this.outputStack = [];
    this.requestUpdate();
  }

  __testWebsocketConnection() {
    this.socket.emit('test');
  }

  __websocketConnectionRsvp() {
    this.socket.emit('json', this.kafkaOffset, newOffset => {
      this.__outputLogger([`RSVP, Updated offset: ${newOffset}`]);
      this.kafkaOffset = newOffset;
    });
  }

  __getHtmlTemplate() {
    return html` <header>Welcome to this fun single page application</header>

      <!-- Heading -->
      <h1>Where You Should Fly Next 🚀</h1>
      <p>
        An application to see which events people around the world are going to
        attend. Bassed on RSVPs
        <a href="https://meetup.com" target="_blank">Meetup.com</a>.
      </p>
      <br />

      <!-- Action Buttons -->
      <div style="margin: 20px">
        <center>
          <button @click=${this.__testWebsocketConnection}>
            Test Connection
          </button>
          <button @click=${this.__websocketConnectionRsvp}>Check RSVPs</button>
          <button @click=${this.__cleanOutput}>Clean Logs</button>
        </center>
      </div>

      <!-- Action Buttons -->
      <div
        style="max-height: 40vh; overflow-y: auto; margin: 20px; padding: 20px; background-color:#f1f1f1; color: crimson;"
      >
        ${this.outputStack.map(
          o =>
            html`<code>${o}</code>
              <hr />`
        )}
      </div>

      <!-- Footer -->
      <center>（￣︶￣）↗</center>`;
  }

  render() {
    return html` ${this.__getHtmlTemplate()} `;
  }
}

// Complete Socket Implementation

// const socket = io('http://localhost:5000');
// socket.on('connect', () => {
//   console.log('Connected to server');
// });
// socket.on('message', (message) => {
//   console.log('Received message: ' + message);
// });

// function sendMessage() {
//   const input = document.getElementById('input').value;
//   socket.send(input);
// }
