import {Injectable} from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class CommonDataService {

    constructor() {
    }
    clientUserId: string = "";
    servers: any[] = []
    // key:id,content:serverInfo
    serverIndexById: Map<string, any> = new Map()
    // key: channelId, content: channelInfo
    channelIndexById: Map<string, any> = new Map();
    // key: userInfoId, content: userInfo
    userInfoIndexById: Map<string, any> = new Map();

    hasUserInfo(id: string) {
        return this.userInfoIndexById.has(id)
    }

    getUserInfo(id: string) {
        return this.userInfoIndexById.get(id)?.data
    }

    public getServerInfoById(serverId: string) {
        return this.serverIndexById.get(serverId);
    }

    public addServerDetails(serverId: string, data: Record<string, any>) {
        const serverInfo = this.getServerInfoById(serverId);
        if (!serverInfo) {
            throw new Error(`Server with ID ${serverId} not found.`);
        }

        // 设置 details 并处理 channel 信息
        serverInfo['details'] = data;

        data['channel_groups']?.forEach((group: any) => {
            group['channels']?.forEach((channel: any) => {
                this.channelIndexById.set(channel['id'], channel);
            });
        });

        return serverInfo['details'];
    }


    public getChannelInfoById(channelId: string) {
        return this.channelIndexById.get(channelId);
    }


    public getServerDetails(serverId: string) {
        return this.getServerInfoById(serverId)['details']
    }


}
