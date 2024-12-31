import {AfterViewChecked, AfterViewInit, Component, ElementRef, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {NgClass, NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {Subscription} from "rxjs";
import {SocketService} from "../../services/socket.service";
import {CommonDataService} from "../../services/common-data.service";
import {ActivatedRoute, Route} from "@angular/router";
import {RequestService} from "../../services/request.service";
import {SessionListComponent} from "../../components/session-list/session-list.component";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    NgOptimizedImage,
    NgForOf,
    SessionListComponent,
    NgIf,
    FormsModule,
    NgClass
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements OnInit, OnDestroy, AfterViewChecked {

  @ViewChild('chatContent') chatContent!: ElementRef;

  subscriptions: Subscription[] = [];

  sessionName = '';
  messageList: any[] = [];
  sessionId: string | null = null;
  sessionType: string | null = null;
  scrollToBottomFlag: boolean = false;
  massageInputValue = "";

  constructor(private requestService: RequestService, private socketService: SocketService, protected commonDataService: CommonDataService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    const newMassageSubject = this.socketService.getMessageSubject("chat", "new_message").subscribe(
      message => {
        this.requestService.getUserDataFromServer(message['id']).then()
        this.messageList.push(message)
        this.scrollToBottomFlag = true;
      })
    this.subscriptions.push(newMassageSubject);
  }

  ngOnDestroy() {
    this.subscriptions.forEach(subscription => subscription.unsubscribe());
  }

  onScroll(event: any) {
    const element = event.target;
    if (element.scrollTop === 0) {
      const previousHeight = element.scrollHeight;
      this.getMessageFromHistory()
      const newHeight = element.scrollHeight;
      element.scrollTop = newHeight - previousHeight;
    }
  }

  getMessageFromHistory() {
    this.requestService.getMessageFromHistory(this.messageList[0], this.sessionId).then(r => {
      this.messageList = r.concat(this.messageList);
    })
  }

  sendMessage() {
    if (this.massageInputValue) {
      this.messageList.push({
        "user_id": '1',
        "content": this.massageInputValue
      })
      // this.requestService.sendMessage(this.sessionId, this.massageInputValue)
      this.massageInputValue = ""
      this.scrollToBottomFlag = true;
    }
  }

  scrollToBottom(): void {
    if (this.chatContent) {
      const element = this.chatContent.nativeElement;
      element.scrollTop = element.scrollHeight; // 滚动到底部
    }
  }


  handleSessionSelected($event: { sessionId: string | null; sessionType: string | null }) {
    this.sessionId = $event.sessionId;
    if ($event.sessionId) {
      if ($event.sessionType) {
        this.sessionName = this.commonDataService.getChannelInfoById($event.sessionId)['name']
      }
      this.requestService.getMessage($event.sessionId).then(r => {
        this.messageList = r;
        const userIdList: any = []
        r.forEach((message: any) => {
          userIdList.push(message.user_id)
        })
        this.requestService.getUserDataFromServer(userIdList).then(r => {
          this.scrollToBottomFlag = true;
        })
      });
    }
  }

  ngAfterViewChecked(): void {
    if (this.scrollToBottomFlag) {
      this.scrollToBottom(); // 每次视图更新后滚动到底部
      this.scrollToBottomFlag = false;
    }
  }


}
