import {Component, EventEmitter, Output} from '@angular/core';
import {RequestService} from "../../services/request.service";
import {Router} from "@angular/router";
import {VoiceChatService} from "../../services/voice-chat.service";
import {CommonDataService} from "../../services/common-data.service";
import {NgForOf, NgIf, NgOptimizedImage} from "@angular/common";

@Component({
    selector: 'app-session-list',
    standalone: true,
    imports: [
        NgIf,
        NgForOf,
        NgOptimizedImage
    ],
    templateUrl: './session-list.component.html',
    styleUrl: './session-list.component.css'
})
export class SessionListComponent {
    @Output() sessionSelected = new EventEmitter<{ sessionId: string | null, sessionType: string | null }>();
    serverInfo: Record<string, any> | undefined;
    protected serverId: string = "";

    constructor(protected commonDataService: CommonDataService, private requestService: RequestService, private router: Router, private voiceChatService: VoiceChatService) {
    }

    public async getServerChannels(serverId: string) {
        this.serverId = serverId;
        await this.requestService.getServerChannels(serverId)
        this.serverInfo = this.commonDataService.getServerInfoById(serverId)
        if (this.serverInfo) {
            console.log(this.serverInfo['channels']);
        }
    }


    backToSessionList() {
        this.serverInfo = undefined
        this.sessionSelected.emit({sessionId: null, sessionType: null});  // 向父组件传递数据
    }

    toChat(channelId: any, channelType: any) {
        if (channelType == 'text') {
            this.sessionSelected.emit({sessionId: channelId, sessionType: channelType});  // 向父组件传递数据
        } else if (channelType == 'voice') {
            this.voiceChatService.initializeRecorder().then(r => {
                console.log('录音开始');
            })
        }
    }
}
