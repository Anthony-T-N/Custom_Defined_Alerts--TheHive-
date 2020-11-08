# Credits: Sayed

def customTLP(subjectField):
        if subjectField in  config['alertKeyword']:
                config['caseTLP'] == 3
                config['alertTLP'] == 3
                print("Assigned High!")
        else:
                config['caseTLP'] == 2
                config['alertTLP'] == 2
                print("Assinged Medium")

        # Prepare the alert
        #
        sourceRef = str(uuid.uuid4())[0:6]
        alert = Alert(title=subjectField.replace('[ALERT]', ''),
                      tlp         = customTLP(subjectField),
                      tags        = tags,
                      description = body,
                      type        = 'external',
                      source      = fromField,
                      sourceRef   = sourceRef,
                      artifacts   = artifacts)
        # If a case template is specified, use it instead of the tasks
        if len(config['caseTemplate']) > 0:
            case = Case(title=subjectField,
                        tlp          = customField(subjectField), 
                        flag         = False,
                        tags         = config['caseTags'],
                        description  = body,
                        template     = config['caseTemplate'],
                        customFields = customFields)
        else:
            case = Case(title        = subjectField,
                        tlp          = customTLP(subjectField), 
                        flag         = False,
                        tags         = config['caseTags'],
                        description  = body,
                        tasks        = tasks,
                        customFields = customFields)
        # Create the case
        id = None
        response = api.create_case(case)
        if response.status_code == 201:
            newID = response.json()['id']
            log.info('Created case %s' % response.json()['caseId'])
            if len(attachments) > 0:
                for path in attachments:
                    observable = CaseObservable(dataType='file',
                        data    = [path],
                        tlp     = customTLP(subjectField),
                        ioc     = False,
                        tags    = config['caseTags'],
                        message = 'Found as email attachment'
                        )
