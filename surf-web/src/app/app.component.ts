import {Component, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {SocketService} from "./services/socket.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterOutlet, NgIf],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit{
  loadingFlag:boolean = true;
  constructor(protected socket:SocketService) {
  }
  ngOnInit(): void {
    //加载程序
    this.socket.initializeMainConnection('localhost:8000').then(()=>{
      this.loadingFlag=false;
    })
  }
}
