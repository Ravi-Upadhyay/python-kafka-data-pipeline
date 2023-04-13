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
  };

  constructor() {
    super();
    this.header = 'Hey there';
    this.counter = 5;
    this.socket = io('http://localhost:5000');
    // this.socket.onopen = () => {
    //   console.log('Websocket connection established');
    // }
    this.socket.on('connect', () => {
      console.log('Connected to server', 'Socket id: ', this.socket.id);
    });
    // this.socket.on('message', (message) => {
    //   console.log('Received Message', message);
    // });
  }

  __increment() {
    this.counter += 1;
  }

  render() {
    return html`
      <h2>${this.header} Nr. ${this.counter}!</h2>
      <button @click=${this.__increment}>increment</button>
    `;
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
