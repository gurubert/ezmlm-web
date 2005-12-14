<div class="info">

<!-- posting moderation -->
<?cs if:Data.List.hasPostMod ?>
    <p class="<?cs if:Data.List.PostModPath ?>warning<?cs else ?>ok<?cs /if ?>"><?cs var:Lang.Misc.Posting ?>
	<?cs if:Data.List.PostModPath ?>
	    <?cs var:Lang.Misc.PostModPathWarn ?>(<?cs var:Data.List.PostModPath ?>). <?cs var:SuggestEdit ?>
	<?cs /if ?>
    </p>
<?cs /if ?>

<!-- subscription moderation -->
<?cs if:Data.List.hasSubMod ?>
    <p class="<?cs if:Data.List.SubModPath ?>warning<?cs else ?>ok<?cs /if ?>"><?cs var:Lang.Misc.Subscription ?>
	<?cs if:Data.SubModPath ?>
	    <?cs var:Lang.Misc.SubModPathWarn ?>(<?cs var:Data.List.SubModPath ?>). <?cs var:SuggestEdit ?>
	<?cs /if ?>
    </p>
<?cs /if ?>

<!-- remote administration -->
<?cs if:Data.List.hasRemoteAdmin ?>
    <p class="<?cs if:Data.List.RemoteAdminPath ?>warning<?cs else ?>ok<?cs /if ?>"><?cs var:Lang.Misc.RemoteAdmin ?>
	<?cs if:Data.RemotePath ?>
	    <?cs var:Lang.Misc.RemoteAdminPathWarn ?>(<?cs var:Data.List.RemoteAdminPath ?>). <?cs var:SuggestEdit ?>
	<?cs /if ?>
    </p>
<?cs /if ?>

</div>
