import { Component } from '@angular/core';
import {SessionListComponent} from "../../../components/session-list/session-list.component";
import {RouterOutlet} from "@angular/router";

@Component({
  selector: 'app-session',
  standalone: true,
  imports: [
    SessionListComponent,
    RouterOutlet
  ],
  templateUrl: './session.component.html',
  styleUrl: './session.component.css'
})
export class SessionComponent {

}
