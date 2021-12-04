#include <iostream>
#include <string.h>
#include <stdlib.h>

using namespace std;

class Produto{
private:
    int *vetCodigo;
    string *vetNome;
    double *vetPreco;
    int *vetQuantidadeNoEstoque;
    int maxTam;


protected:
    int codigo, QuantidadeNoEstoque, QuantidadeVendida;
    string nome;
    double preco;

public:
    int ProdutosCadatrados = 0;
    Produto(){
        vetCodigo = new int[100];
        vetNome = new string[100];
        vetPreco = new double[100];
        vetQuantidadeNoEstoque = new int[100];
        maxTam = 99;
    }
    ~Produto(){
        delete[] vetCodigo;
        delete[] vetNome;
        delete[] vetPreco;
        delete[] vetQuantidadeNoEstoque;
    }

    void adicionarProduto(int codigo, string nome, double preco, int QuantidadeNoEstoque){
        this -> codigo = codigo;
        this -> nome = nome;
        this -> preco = preco;
        this -> QuantidadeNoEstoque = QuantidadeNoEstoque;
        setValores(codigo, nome, preco, QuantidadeNoEstoque);
    }

    void setValores(int codigo, string nome, double preco, int QuantidadeNoEstoque){
        vetCodigo[ProdutosCadatrados] = codigo;
        vetNome[ProdutosCadatrados] = nome;
        vetPreco[ProdutosCadatrados] = preco;
        vetQuantidadeNoEstoque[ProdutosCadatrados] = QuantidadeNoEstoque;
        ProdutosCadatrados += 1;
    }

    void getProdutos(){
        for(int i = 0; i < ProdutosCadatrados; i++){
            cout << "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" << endl;
            cout << "Codigo: " << vetCodigo[i] << endl;
            cout << "Nome: " << vetNome[i] << endl;
            cout << "Preco: R$ " << vetPreco[i] << endl;
            cout << "Quantidade no estoque: " << vetQuantidadeNoEstoque[i] << endl;
        }
        cout << "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" << endl;
        menuSucundario();
    }

    void getProdutos(int pesquisa, int controle){
        cout << "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" << endl;
        cout << "Codigo: " << vetCodigo[pesquisa] << endl;
        cout << "Nome: " << vetNome[pesquisa] << endl;
        cout << "Preco: R$ " << vetPreco[pesquisa] << endl;
        cout << "Quantidade no estoque: " << vetQuantidadeNoEstoque[pesquisa] << endl;
        cout << "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" << endl;
        if(controle == 0){
            menuSucundario();
        }
    }

    void menuSucundario(){
        int op;
        cout << "1 Tela De Inicio" << endl << "Opcao: ";
        cin >> op;
    }

    void alterarInformacao(int codigoDePesquisa){
        string nome;
        double preco;
        int QuantidadeNoEstoque;
        getProdutos(codigoDePesquisa, 1);
        cout << "Digite as novas informaçoes: " << endl << endl;
        cout << "Nome: " ;
        cin >> nome;
        cout << "Preco: R$ ";
        cin >> preco;
        cout << "Quantidade no estoque: ";
        cin >> QuantidadeNoEstoque;
        cout << "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" << endl;
        vetNome[codigoDePesquisa] = nome;
        vetPreco[codigoDePesquisa] = preco;
        vetQuantidadeNoEstoque[codigoDePesquisa] = QuantidadeNoEstoque;
    }

    void ExcluirProduto(int codigo){
        while(codigo < ProdutosCadatrados){
            vetCodigo[codigo] = vetCodigo[codigo];
            vetNome[codigo] = vetNome[codigo+1];
            vetPreco[codigo] = vetPreco[codigo+1];
            vetQuantidadeNoEstoque[codigo] = vetQuantidadeNoEstoque[codigo+1];
            codigo++;
        }
        ProdutosCadatrados -=1;
    }
};

void TelaInicial(){
    system("clear");
    cout << " ==== Contre de estoque ===" << endl;
    cout << "1 Cadastrar Produto" << endl;
    cout << "2 Ver Produtos Cadastrados" << endl ;
    cout << "3 Modificar Informaçoes de Algum Produto" << endl;
    cout << "4 Excluir Produto" << endl;
    cout << "5 Sair do Programa" <<
    endl << "Opcao: ";

}

int main(){
    Produto p;
    int op;
    do{
        TelaInicial();
        cin >> op;
        switch(op){
            case 1:{
                int codigo;
                string nome;
                double preco;
                int QuantidadeNoEstoque;
                system("clear");
                cout << "O codigo do produto sera: " << p.ProdutosCadatrados << endl;
                codigo = p.ProdutosCadatrados;
                cout << "Nome do Produto: ";
                cin >> nome;
                cout << "Preço do produto: ";
                cin >> preco;
                cout << "Quantidade para adicionar no estoque: ";
                cin >> QuantidadeNoEstoque;
                p.adicionarProduto(codigo, nome, preco, QuantidadeNoEstoque);
                break;
                }
            case 2:{
                system("clear");
                string pesquisa;
                cout << "Deseja pesquisar algum produto especifico [S] / [N]: ";
                cin >> pesquisa;
                if(pesquisa == "S" || pesquisa == "s"){
                    do{
                        int codigoPesquisa;
                        cout << "Digite o codigo: ";
                        cin >> codigoPesquisa;
                        if(codigoPesquisa > p.ProdutosCadatrados - 1)
                            cout << "Nenhum produto cadastrado com este codido" << endl;
                        else
                            p.getProdutos(codigoPesquisa, 0);
                            break;
                    }while(1);
                }
                else if (pesquisa == "N" || pesquisa == "n")
                    p.getProdutos();
                else
                    cout << "Escolha invalida";
                break;
                }
            case 3:{
                system("clear");
                int cod;
                cout << "Digeite o codigo do produto que deja realizar a alteraçao: ";
                cin >> cod;
                p.alterarInformacao(cod);
                break;
            }
            case 4:{
                do{
                    string pesquisa;
                    system("clear");
                    int CodigoProdutoExcluido;
                    cout << "Informe o codigo do produto a ser excluido do sistema: ";
                    cin >> CodigoProdutoExcluido;
                    if(CodigoProdutoExcluido > p.ProdutosCadatrados - 1)
                        cout << "Nenhum produto cadastrado com este codido" << endl;
                    else
                        p.getProdutos(CodigoProdutoExcluido, 1);
                        cout << "Deseja realmente excluir o registro do produto [S] / [N]:";
                        cin >> pesquisa;
                        if(pesquisa == "S" || pesquisa == "s"){
                            p.ExcluirProduto(CodigoProdutoExcluido);
                            break;
                        }
                        else
                            break;
                    }while(1);
            }
            case 5:{
                break;
            }
            default:{
                cout << "Op invalida";
                }
        }
    }while(op != 5);
    return 0;
}
