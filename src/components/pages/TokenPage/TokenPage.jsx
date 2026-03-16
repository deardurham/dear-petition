import styled from 'styled-components';
import PageBase from '../PageBase';
import { Button } from '../../elements/Button';
import { useObtainAuthTokenQuery, useCreateAuthTokenQuery } from '../../../service/api';

const TokenPageStyled = styled(PageBase)`
  display: flex;
`;

const TokenPageContent = styled.div`
  width: 75%;
  max-width: 1200px;
  min-width: 400px;
  padding: 2rem;
`;

const TokenSection = styled.div`
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
`;

const TokenDisplay = styled.div`
  background: #ffffff;
  border: 1px solid #ced4da;
  border-radius: 4px;
  padding: 1rem;
  font-family: 'Courier New', monospace;
  word-break: break-all;
  margin: 1rem 0;
  font-size: 1.5rem;
`;

const InstructionText = styled.div`
  margin-bottom: 1.5rem;
  line-height: 1.6;

  h2 {
    color: #495057;
    margin-bottom: 0.5rem;
  }

  p {
    margin-bottom: 1rem;
    color: #6c757d;
  }

  ul {
    padding-left: 1.5rem;
    color: #6c757d;
  }

  li {
    margin-bottom: 0.5rem;
  }
`;

const ErrorMessage = styled.div`
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f1aeb5;
  border-radius: 4px;
  padding: 1rem;
  margin: 1rem 0;
`;

export default function TokenPage() {
  const {
    data: existingTokenData,
    isLoading: isLoadingExisting,
    error: existingTokenError,
  } = useObtainAuthTokenQuery();
  const {
    data: newTokenData,
    isLoading: isCreating,
    error: createError,
    refetch: createToken,
  } = useCreateAuthTokenQuery();
  const tokenData = newTokenData || existingTokenData;
  const token = tokenData?.token;
  const isLoading = isLoadingExisting || isCreating;

  const hasCreateError = createError && (createError.status || createError.data);
  const hasExistingError = existingTokenError && (existingTokenError.status || existingTokenError.data);
  const error = hasCreateError ? createError : hasExistingError ? existingTokenError : null;

  const handleCreateToken = () => {
    createToken();
  };

  return (
    <TokenPageStyled>
      <TokenPageContent>
        <InstructionText>
          <h2>API Authentication Token</h2>
          <p>
            Your API authentication token allows you to create cases in EZ Expunge from other systems (for example
            ZipCase). This token is unique to your account and should be kept secure.
          </p>
          <p>
            <strong>Important Security Guidelines:</strong>
          </p>
          <ul>
            <li>Never share your token with others</li>
            <li>Store it securely in environment variables or secure configuration files</li>
            <li>If you suspect your token has been compromised, generate a new one immediately</li>
          </ul>
        </InstructionText>

        <TokenSection>
          <h3>Your Authentication Token</h3>
          {error && (
            <ErrorMessage>
              Error loading token: {error.message || error.data?.detail || 'Unknown error occurred'}
            </ErrorMessage>
          )}

          {token && <TokenDisplay>{token}</TokenDisplay>}

          <div style={{ marginTop: '1rem' }}>
            <Button onClick={handleCreateToken} disabled={isLoading} style={{ marginRight: '1rem' }}>
              {isLoading ? 'Loading...' : token ? 'Regenerate Token' : 'Generate Token'}
            </Button>

            {token && (
              <Button variant="secondary" onClick={() => navigator.clipboard.writeText(token)}>
                Copy to Clipboard
              </Button>
            )}
          </div>
        </TokenSection>
      </TokenPageContent>
    </TokenPageStyled>
  );
}
