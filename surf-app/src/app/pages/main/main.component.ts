import {Component, OnDestroy, OnInit} from '@angular/core';
import {appDataDir} from "@tauri-apps/api/path";
import {invoke} from "@tauri-apps/api/core";
import {Router, RouterOutlet} from "@angular/router";
import {NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {CommonDataService} from "../../services/common-data.service";
import {SocketService} from "../../services/socket.service";
import {Subscription} from "rxjs";
import {VoiceChatService} from "../../services/voice-chat.service";
import {RequestService} from "../../services/request.service";
import {ChatComponent} from "../chat/chat.component";

@Component({
  selector: 'app-main',
  standalone: true,
    imports: [
        RouterOutlet,
        NgOptimizedImage,
        NgForOf,
        NgIf,
        ChatComponent
    ],
  templateUrl: './main.component.html',
  styleUrl: './main.component.css'
})
export class MainComponent implements OnInit, OnDestroy {
    subscriptions: Subscription[] = [];

    ngOnDestroy() {
        this.subscriptions.forEach(subscription => subscription.unsubscribe());
    }

    constructor(
        protected requestService: RequestService,
        private router: Router,
        private socketService: SocketService,
        protected commonDataService: CommonDataService,
        private voiceChatService: VoiceChatService) {
    }

    ngOnInit(): void {
        if (!this.socketService.isConnected()) {
            this.router.navigate(['/']).then();
            return
        }
        // this.requestService.getUserData();
        this.requestService.requestUserServers();
    }

    toUserInfo() {
        this.router.navigate(['/main/user-info']).then();
    }

    toSettings() {
        this.router.navigate(['/main/settings']).then();
    }

    toChat() {
        this.router.navigate(['/main/chat']).then();
    }
}
