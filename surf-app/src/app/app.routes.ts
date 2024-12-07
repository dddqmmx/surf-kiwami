import {Routes} from "@angular/router";
import {LoginComponent} from "./pages/login/login.component";
import {MainComponent} from "./pages/main/main.component";
import {ChatComponent} from "./pages/chat/chat.component";
import {SettingsComponent} from "./pages/settings/settings.component";
import {UserInfoComponent} from "./pages/user-info/user-info.component";

export const routes: Routes = [
    {path: '', component: LoginComponent},
    {
        path: 'main', component: MainComponent, children: [
            {path: "chat", component: ChatComponent},
            {path: "settings", component: SettingsComponent},
            {path: "user_info", component: UserInfoComponent}
        ]
    }
];
