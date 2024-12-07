import {Component, OnDestroy, OnInit} from '@angular/core';
import {NgForOf, NgOptimizedImage} from "@angular/common";
import {Router} from "@angular/router";
import {TitleBarComponent} from "../../components/title-bar/title-bar.component";
import {appDataDir} from "@tauri-apps/api/path";
import {invoke} from "@tauri-apps/api/core";
import {FormsModule} from "@angular/forms";
import {SocketService} from "../../services/socket.service";
import {connect, Subscription} from "rxjs";
import {CommonDataService} from "../../services/common-data.service";
import {RequestService} from "../../services/request.service";

interface User {
    name: string;
    file: string;
    // 其他用户属性可以根据需要添加
}

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [
        NgOptimizedImage,
        TitleBarComponent,
        NgForOf,
        FormsModule
    ],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit, OnDestroy {
    constructor(
        private requestService: RequestService,
        private router: Router,
        private socket: SocketService,
        private commonData: CommonDataService) {
    }

    subscriptions: Subscription[] = [];

    ngOnDestroy() {
        this.subscriptions.forEach(subscription => subscription.unsubscribe());
    }

    users: User[] = []
    selectedUserPath = "";

    ngOnInit(): void {
        this.loadUserProfiles();
    }

    async processProfiles(profiles: unknown) {
        if (typeof profiles !== "string") {
            console.error("Invalid profiles data");
            return;
        }

        const profilesJson = JSON.parse(profiles);
        this.users = profilesJson['user-keys'] || [];

        const automaticLogin: number = profilesJson['automatic-login']
        if (automaticLogin != null) {
            console.log(automaticLogin)
            this.selectedUserPath = this.users[automaticLogin].file;
            await this.login()
        }

        // 设置默认选中第一个用户
        if (this.users.length > 0) {
            this.selectedUserPath = this.users[0].file;
        }
    }

    async login() {
        if (!this.selectedUserPath) {
            console.error('No user selected');
            return;
        }

        console.log('Selected user path:', this.selectedUserPath);

        try {
            const dir = await appDataDir();  // 获取应用数据目录
            const filePath = `${dir}\\keys\\${this.selectedUserPath}`;
            console.log(filePath);

            const profiles = await invoke("read_file", {path: filePath});

            if (typeof profiles !== "string") {
                console.error("Invalid profile data");
                return;
            }

            const userFile = JSON.parse(profiles);
            const isConnected = await this.socket.initializeMainConnection(userFile['server_address']);

            if (!isConnected) {
                console.error("Failed to connect to the server.");
                return;
            }

            this.requestService.loginAndSubscribe(userFile)

        } catch (error) {
            console.error("Error during login process:", error);
        }
    }

    private async loadUserProfiles() {
        try {
            const dir = await appDataDir();
            const profiles = await invoke("read_file", {path: `${dir}\\user-profiles.json`});
            await this.processProfiles(profiles);
        } catch (error) {
            console.error("Error during initialization:", error);
        }
    }
}
