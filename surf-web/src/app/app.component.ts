import {Component, OnInit} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {SocketService} from "./services/socket.service";
import {NgIf} from "@angular/common";
import {RequestService} from "./services/request.service";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterOutlet, NgIf],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  loadingFlag: boolean = false;

  constructor(protected socket: SocketService, private requestService: RequestService) {
  }

  ngOnInit(): void {
    //加载程序
    this.socket.initializeMainConnection('localhost:8000').then(() => {
      this.loadingFlag = false;
      // 初始化时加载存储的值
      const storedUsername = localStorage.getItem('username') || '';
      const storedPassword = localStorage.getItem('password') || '';
      const storedRememberMe = localStorage.getItem('rememberMe') || '';

      if (storedRememberMe === 'true') {
        this.requestService.requestLogin(storedUsername, storedPassword)
      }
    })
  }
}
