import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { MaterialModule } from '@angular/material';
import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { SidenavComponent } from './components/sidenav/sidenav.component';
import { HomeComponent } from './views/home/home.component';
import { LoginComponent } from './views/login/login-view.component';
import { DynamicComponentComponent } from './components/dynamic-component/dynamic-component.component';
import { RiriComponent } from './components/widgets/riri/riri.component';
import { FifiComponent } from './components/widgets/fifi/fifi.component';
import { LoulouComponent } from './components/widgets/loulou/loulou.component';
import { PokechonHomeComponent } from './views/pokechon-home/pokechon-home.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SidenavComponent,
    HomeComponent,
    LoginComponent,
    DynamicComponentComponent,
    RiriComponent,
    FifiComponent,
    LoulouComponent,
    PokechonHomeComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterialModule.forRoot(),
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
