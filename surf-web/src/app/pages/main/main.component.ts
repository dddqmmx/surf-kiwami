import {Component, OnDestroy, OnInit} from '@angular/core';
import {Router, RouterOutlet} from "@angular/router";
import {NgClass, NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
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
        ChatComponent,
        NgClass
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

    options = [
        { name: 'userInfo', icon: '/images/avatar/default-avatar.png', height: 38, width: 38 },
        { name: 'chat', icon: '/images/icon/chat_bubble.svg', height: 38, width: 38 },
        { name: 'groups', icon: '/images/icon/groups.svg', height: 38, width: 38 },
        { name: 'campaign', icon: '/images/icon/campaign.svg', height: 38, width: 38 },
        { name: 'person', icon: '/images/icon/person.svg', height: 38, width: 38 },
        { name: 'call', icon: '/images/icon/call.svg', height: 38, width: 38 },
        { name: 'settings', icon: '/images/icon/settings.svg', height: 38, width: 38 },
    ];

    selectedOption: string = '';  // 记录当前选中的选项

    // 处理选择操作，更新 selectedOption
    onSelect(option: any) {
        this.selectedOption = option.name;
        switch (option.name){
            case 'userInfo':{
                this.router.navigate(['/main/user-info']).then();
                break
            }
            case 'chat':{
                this.router.navigate(['/main/chat']).then();
                break
            }
            case 'settings':{
                this.router.navigate(['/main/settings']).then();
                break
            }
        }
    }

    ngOnInit(): void {
        // if (!this.socketService.isConnected()) {
        //     this.router.navigate(['/']).then();
        //     return
        // }
        // this.requestService.getUserData();
        this.requestService.requestUserServers();
    }

}
