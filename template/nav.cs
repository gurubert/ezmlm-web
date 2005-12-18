<!-- $Id$ -->

<div id="nav">

<?cs if:Data.List.Name ?>

	<ul class="list_config">
		<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers" title="<?cs var:Lang.Menue.Subscribers ?>"><?cs var:Lang.Menue.Subscribers ?></a>
			<ul>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers&part=allow"><?cs var:Lang.Menue.AllowList ?></a></li>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers&part=deny"><?cs var:Lang.Menue.DenyList ?></a></li>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers&part=digest"><?cs var:Lang.Menue.DigestList ?></a></li>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers&part=mod"><?cs var:Lang.Menue.ModList ?></a></li>
			</ul>
		</li>

		<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=main" title="<?cs var:Lang.Menue.ConfigMain ?>"><?cs var:Lang.Menue.ConfigMain ?></a>
			<ul>
				<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=subscription" title="<?cs var:Lang.Menue.ConfigSub ?>"><?cs var:Lang.Menue.ConfigSub ?></a></li>
				<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=posting" title="<?cs var:Lang.Menue.ConfigPost ?>"><?cs var:Lang.Menue.ConfigPost ?></a></li>
				<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=filter" title="<?cs var:Lang.Menue.ConfigFilter ?>"><?cs var:Lang.Menue.ConfigFilter ?></a></li>
				<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=archive" title="<?cs var:Lang.Menue.ConfigArchive ?>"><?cs var:Lang.Menue.ConfigArchive ?></a></li>
				<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=admin" title="<?cs var:Lang.Menue.ConfigAdmin ?>"><?cs var:Lang.Menue.ConfigAdmin ?></a></li>
			</ul>
		</li>

		<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=textfiles" title="<?cs var:Lang.Menue.TextFiles ?>"><?cs var:Lang.Menue.TextFiles ?></a></li>

		<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=list_delete_ask" title="<?cs var:Lang.Menue.Delete ?>"><?cs var:Lang.Menue.Delete ?></a></li>
		
	</ul>

<?cs /if ?>

<hr/>

<ul class="all_lists">
	<?cs if:Data.Permissions.Create ?>
		<li><a href="<?cs var:ScriptName ?>?action=list_create_ask" title="<?cs var:Lang.Menue.Create ?>"><?cs var:Lang.Menue.Create ?></a></li>
	<?cs /if ?>
	<?cs if:subcount(Data.Lists) > 0 ?>
		<li><?cs var:Lang.Menue.AvailableLists ?>
			<ul>
				<?cs each:item = Data.Lists ?>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(item) ?>&action=subscribers"><?cs var:item ?></a></li>
				<?cs /each ?>
		</ul></li>
	<?cs /if ?>
</ul>

</div>
