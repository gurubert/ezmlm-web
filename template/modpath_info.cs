<div class="info">

<!-- posting moderation -->
<?cs if:Data.isPostMod ?>
    <p class="<?cs if:Data.PostModPath ?>warning<?cs else ?>ok<?cs /if ?>"><?cs var:Lang.Misc.Posting ?>
	<?cs if:Data.PostModPath ?>
	    <?cs var:Lang.Misc.PostModPathWarn ?>(<?cs var:Data.PostModPath ?>). <?cs var:SuggestEdit ?>
	<?cs /if ?>
    </p>
<?cs /if ?>

<!-- subscription moderation -->
<?cs if:Data.isSubMod ?>
    <p class="<?cs if:Data.SubModPath ?>warning<?cs else ?>ok<?cs /if ?>"><?cs var:Lang.Misc.Subscription ?>
	<?cs if:Data.SubModPath ?>
	    <?cs var:Lang.Misc.SubModPathWarn ?>(<?cs var:Data.SubModPath ?>). <?cs var:SuggestEdit ?>
	<?cs /if ?>
    </p>
<?cs /if ?>

<!-- remote administration -->
<?cs if:Data.isRemote ?>
    <p class="<?cs if:Data.RemotePath ?>warning<?cs else ?>ok<?cs /if ?>"><?cs var:Lang.Misc.RemoteAdmin ?>
	<?cs if:Data.RemotePath ?>
	    <?cs var:Lang.Misc.RemotePathWarn ?>(<?cs var:Data.RemotePath ?>). <?cs var:SuggestEdit ?>
	<?cs /if ?>
    </p>
<?cs /if ?>

</div>
