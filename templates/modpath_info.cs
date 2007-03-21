<!-- posting moderation -->
<?cs if:Data.List.hasCustomizedPostModPath ?>
    <div class="warning">
	    <?cs var:html_escape(Lang.Misc.PostModPathWarn) ?> (<?cs var:Data.List.Settings.7.value ?>).<br/><?cs var:html_escape(Lang.Misc.SuggestDefaultPath) ?>
    </div>
<?cs /if ?>

<!-- subscription moderation -->
<?cs if:Data.List.hasCustomizedSubModPath ?>
    <div class="warning">
	    <?cs var:html_escape(Lang.Misc.SubModPathWarn) ?> (<?cs var:Data.List.Settings.8.value ?>).<br/><?cs var:html_escape(Lang.Misc.SuggestDefaultPath) ?>
    </div>
<?cs /if ?>

<!-- remote administration -->
<?cs if:Data.List.hasCustomizedAdminPath ?>
    <div class="warning">
	    <?cs var:html_escape(Lang.Misc.RemoteAdminPathWarn) ?> (<?cs var:Data.List.Settings.9.value ?>).<br/><?cs var:html_escape(Lang.Misc.SuggestDefaultPath) ?>
    </div>
<?cs /if ?>
