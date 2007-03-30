<!-- $Id$ -->

<?cs include:TemplateDir + '/macros.cs' ?>
<?cs include:TemplateDir + '/header.cs' ?>

<!-- this ezmlm-web template follows: <?cs var:Data.Action ?> -->

<?cs include:TemplateDir + '/nav.cs' ?>
<div id="main_content">
	<?cs if:Data.List.Name ?><div id="info_title"><?cs
		if:Data.CurrentDomain ?><?cs
			var:html_escape(Data.CurrentDomain.Description) ?> - <?cs /if
		?><?cs var:html_escape(Data.List.Name) ?> - <?cs
			var:html_escape(Data.List.Address) ?></div><?cs /if ?>
	<?cs if:Data.Error ?><?cs call:error(Lang.ErrorMessage[Data.Error]) ?><?cs /if ?>
	<?cs if:Data.customError ?><?cs call:error(Data.customError) ?><?cs /if ?>
	<?cs if:Data.Warning ?><?cs call:warning(Lang.WarningMessage[Data.Warning]) ?><?cs /if ?>
	<?cs if:Data.customWarning ?><?cs call:warning(Data.customWarning) ?><?cs /if ?>
	<?cs if:Data.Success ?><?cs call:success(Lang.SuccessMessage[Data.Success]) ?><?cs /if ?>
	<?cs include:TemplateDir + '/' + Data.Action + '.cs' ?>
</div> <!-- end of main_content -->

<?cs include:TemplateDir + '/footer.cs' ?>

