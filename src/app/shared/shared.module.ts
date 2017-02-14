import { NgModule } from '@angular/core';

import { OverlayComponent } from './overlay.component';
import { FullscreenDirective } from './fullscreen.directive';

@NgModule({
    imports: [],
    exports: [
        OverlayComponent,
        FullscreenDirective
    ],
    declarations: [
        OverlayComponent,
        FullscreenDirective
    ]
})
export class SharedModule {}