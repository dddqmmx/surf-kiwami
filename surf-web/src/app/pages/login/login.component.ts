import {Component, OnDestroy, OnInit} from '@angular/core';
import {NgForOf, NgOptimizedImage} from "@angular/common";
import {Router} from "@angular/router";
import {FormsModule} from "@angular/forms";
import {SocketService} from "../../services/socket.service";
import {connect, Subscription} from "rxjs";
import {CommonDataService} from "../../services/common-data.service";
import {RequestService} from "../../services/request.service";

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [
        NgOptimizedImage,
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
    account: string | undefined;
    password: string | undefined;

    ngOnDestroy() {
        this.subscriptions.forEach(subscription => subscription.unsubscribe());
    }


    ngOnInit(): void {
    }

    login(){
        this.socket.initializeMainConnection('localhost:8000').then(()=>{
          this.requestService.requestLogin(this.account,this.password)
        })
    }

    toManageUsers() {
        this.router.navigate(['/manage-users']).then();
    }
}
