import { Component } from '@angular/core';
import {NgOptimizedImage} from "@angular/common";
import {RouterOutlet} from "@angular/router";

@Component({
  selector: 'app-contacts',
  standalone: true,
  imports: [
    NgOptimizedImage,
    RouterOutlet
  ],
  templateUrl: './contacts.component.html',
  styleUrl: './contacts.component.css'
})
export class ContactsComponent {

}
