import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CodexComponent } from './views/codex/codex.component';
import { WelcomeComponent } from './views/welcome/welcome.component';
import { PokechonCardComponent } from './components/pokechon-card/pokechon-card.component';

const routes: Routes = [
    { path: '', component: CodexComponent }
];

@NgModule({
    exports: [],
    imports: [
        RouterModule.forChild(routes)
    ],
    declarations: [CodexComponent, WelcomeComponent, PokechonCardComponent],
    providers: [],
    entryComponents: []
})
export class PokechonModule {}
