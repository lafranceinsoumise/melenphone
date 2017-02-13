import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { CodexComponent } from './views/codex/codex.component';
import { WelcomeComponent } from './views/welcome/welcome.component';
import { PokechonCardComponent } from './components/pokechon-card/pokechon-card.component';

import { PokechonCardService } from './common/pokechon-card.service';

const routes: Routes = [
    { path: '', component: CodexComponent }
];

@NgModule({
    exports: [],
    imports: [
        RouterModule.forChild(routes),
        CommonModule
    ],
    declarations: [CodexComponent, WelcomeComponent, PokechonCardComponent],
    providers: [PokechonCardService],
    entryComponents: []
})
export class PokechonModule {}
