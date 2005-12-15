<!-- $Id$ -->

<div id="nav">

<?cs if:Data.List.Name ?>

	<ul class="list_config">
		<li><a href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=subscribers" name="<?cs var:Lang.Menue.Subscribers ?>"><?cs var:Lang.Menue.Subscribers ?></a></li>
			<?cs if:(Data.List.hasAllowList || Data.List.hasDenyList || Data.List.hasDigestList) ?>
				<ul>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=subscribers&part=allow" name="<?cs var:Lang.Menue.AllowList ?>"><?cs var:Lang.Menue.AllowList ?></a></li>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=subscribers&part=deny" name="<?cs var:Lang.Menue.DenyList ?>"><?cs var:Lang.Menue.DenyList ?></a></li>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=subscribers&part=digest" name="<?cs var:Lang.Menue.DigestList ?>"><?cs var:Lang.Menue.DigestList ?></a></li>
				</ul>
			<?cs /if ?>
		</li>

		<li><a href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=config_main_ask" name="<?cs var:Lang.Menue.ConfigMain ?>"><?cs var:Lang.Menue.ConfigMain ?></a></li>
		<ul>
			<li><a href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=config_subscription_ask" name="<?cs var:Lang.Menue.ConfigSub ?>"><?cs var:Lang.Menue.ConfigSub ?></a></li>
			<li><a href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=config_posting_ask" name="<?cs var:Lang.Menue.ConfigPost ?>"><?cs var:Lang.Menue.ConfigPost ?></a></li>
			<li><a href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=config_admin_ask" name="<?cs var:Lang.Menue.ConfigAdmin ?>"><?cs var:Lang.Menue.ConfigAdmin ?></a></li>
		</ul>

		<li><a href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=textfiles" name="<?cs var:Lang.Menue.TextFiles ?>"><?cs var:Lang.Menue.TextFiles ?></a></li>

		<li><a href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_delete_ask" name="<?cs var:Lang.Menue.Delete ?>"><?cs var:Lang.Menue.Delete ?></a></li>
		
	</ul>

<?cs /if ?>

<hr/>

<ul class="all_lists">
	<?cs if:Data.Permissions.Create ?>
		<li><a href="<?cs var:ScriptName ?>?action=list_create_ask" name="<?cs var:Lang.Menue.Create ?>"><?cs var:Lang.Menue.Create ?></a></li>
	<?cs /if ?>
	<?cs if:Data.ListsCount > 0 ?>
		<li><?cs var:Lang.Menue.AvailableLists ?>
			<ul>
				<?cs each:item = Data.Lists ?>
					<li><a href="<?cs var:ScriptName ?>?list=<?cs var:item ?>&action=subscribers" name="choose list <?cs var:item ?>"><?cs var:item ?></a></li>
				<?cs /each ?>
			</ul>
		</li>
	<?cs /if ?>
</ul>

</div>
