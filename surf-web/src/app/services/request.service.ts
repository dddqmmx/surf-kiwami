// 在 RequestService 中
import {Injectable} from '@angular/core';
import {Router} from '@angular/router';
import {SocketService} from './socket.service'; // 假设您的 SocketService 是这个路径
import {CommonDataService} from './common-data.service';
import {first, firstValueFrom, map} from "rxjs";
@Injectable({
    providedIn: 'root'
})
export class RequestService {
    constructor(
        private socket: SocketService,
        private router: Router,
        private commonData: CommonDataService
    ) {
    }

    sendMessage(sessionId: any, massageInputValue: any) {
        this.socket.send("chat", "send_message", {
            "message": {
                "channel_id": sessionId,
                "content": massageInputValue,
            }
        })
    }

    getMessageFromHistory(oldestMessage: any, sessionId: any) {
        const getMessageResultObservable = this.socket.getMessageSubject("chat", "get_message_result");
        this.socket.send("chat", "get_message", {
            "channel_id": sessionId,
            "last_msg": [oldestMessage.chat_time, oldestMessage.chat_id]
        })
        return firstValueFrom(getMessageResultObservable)
    }



    async getUserDataFromServer(ids: string[]): Promise<Map<string, any>> {
        const now = Date.now();
        const result = new Map<string, any>();
        const idsToFetch: string[] = [];

        // 使用 Set 去重
        const uniqueIds = Array.from(new Set(ids));

        uniqueIds.forEach((id: string) => {
            const userInfo = this.commonData.userInfoIndexById.get(id);
            if (userInfo && (now - userInfo.timestamp < 30 * 60 * 1000)) {
                // 如果数据存在且未超过30分钟，使用缓存的数据
                result.set(id, userInfo.data);
            } else {
                // 需要重新获取的数据
                idsToFetch.push(id);
            }
        });

        if (idsToFetch.length > 0) {
            // 发送请求以获取用户数据
            this.socket.send('user', 'search_user', {
                'user_id_list': idsToFetch
            });

            // 返回一个 Promise 来等待响应
            await new Promise<void>((resolve) => {
                // 订阅响应消息
                this.socket.getMessageSubject('user', 'search_user_result').pipe(
                    first()  // 只获取一次消息并取消订阅
                ).subscribe((message: any[]) => {
                    const now = Date.now();
                    message.forEach((item: any) => {
                        // 更新缓存
                        this.commonData.userInfoIndexById.set(item.user_id, {data: item, timestamp: now});
                        result.set(item.user_id, item);
                    });
                    resolve();  // 确保完成时调用 resolve
                });
            });
        }

        // 返回已准备好的数据
        return result;
    }

    public requestUserServers() {
        this.socket.request('user', 'get_user_servers').then(response => {
            console.log('Received response:', response);
            this.commonData.servers = response['servers_id'];
            this.requestServerInfo()
        }).catch(error => {
            console.error('Request failed:', error);
        });
    }

    public requestServerInfo() {
        this.socket.request('server', 'get_server_info_by_ids', {
            "server_ids": this.commonData.servers
        }).then(response => {
            response['servers_info'].forEach((info: any) => {
                const [key, value] = Object.entries(info)[0];
                this.commonData.serverIndexById.set(key, value);
            })
        }).catch(error => {
            console.error('Request failed:', error);
        });
    }

    public async getMessage(channelId: string | null) {
        const getMessageResultObservable = this.socket.getMessageSubject("chat", "get_message_result");
        this.socket.send("chat", "get_message", {
            "channel_id": channelId,
        })
        return firstValueFrom(getMessageResultObservable); // 如果 Observable 发出的值已经是数
    }

    public async getServerChannels(serverId: string): Promise<Record<string, any>> {
        // 先检查缓存中是否已有数据
        const cachedData = this.commonData.getServerChannels(serverId);
        if (cachedData) {
            return cachedData; // 如果有缓存，直接返回
        }

        // 如果没有缓存，则通过 socket 请求获取数据
        const response = await this.socket.request('server', 'get_server_channels', {
            'server_id': serverId
        });

        // 将数据存入缓存
        this.commonData.addServerChannels(serverId, response['channels']);

        // 返回数据
        return response; // 返回从 socket 获得的数据
    }

    public requestLogin(account: string | undefined, password: string | undefined) {
        this.socket.request('user', 'login', {
            'account':account,
            'password':password
        }).then(response => {
          if (response['id']){
            this.commonData.clientUserId = response['id']
            this.router.navigate(['/main/session']).then();
          }
        }).catch(error => {
            console.error('Request failed:', error);
        });
    }

    public emailCheck(email: string | undefined) {
        this.socket.request('email', 'email_check', {
            'email':email
        }).then(response => {
          console.log(response)
        }).catch(error => {
            console.error('Request failed:', error);
        });
    }

}
