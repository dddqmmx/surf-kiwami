import {Routes} from "@angular/router";
import {LoginComponent} from "./pages/login/login.component";
import {MainComponent} from "./pages/main/main.component";
import {ChatComponent} from "./pages/chat/chat.component";
import {SettingsComponent} from "./pages/main/settings/settings.component";
import {UserInfoComponent} from "./pages/user-info/user-info.component";
import {ManageUsersComponent} from "./pages/manage-users/manage-users.component";
import {SessionComponent} from "./pages/main/session/session.component";
import {ContactsComponent} from "./pages/main/contacts/contacts.component";
import {AccountManageComponent} from "./pages/main/settings/account-manage/account-manage.component";
import {RegisterComponent} from "./pages/register/register.component";
import {GeneralSettingsComponent} from "./pages/main/settings/general-settings/general-settings.component";
import {FriendRequestListComponent} from "./pages/main/contacts/friend-request-list/friend-request-list.component";

export const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch: 'full'},
  {path: 'login', component: LoginComponent},
  {path: "register", component: RegisterComponent},
  {path: 'main', component: MainComponent, children: [
      {path: "contacts", component:ContactsComponent, children:
          [
            {path: "friend_request_list", component: FriendRequestListComponent},
            {path: "user_info", component:UserInfoComponent}
          ]
      },
      {path: "session", component: SessionComponent},
      {path: "chat", component: ChatComponent},
      {path: "settings", component: SettingsComponent, children:
          [
            {path: "account_manage", component:AccountManageComponent},
            {path: "general_settings", component:GeneralSettingsComponent}
          ]
      },
    ]
  }
];
